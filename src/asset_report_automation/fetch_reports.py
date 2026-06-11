from __future__ import annotations

import hashlib
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
import yaml
from bs4 import BeautifulSoup

from .models import CandidateReport, SourceConfig


def load_sources(config_path: Path) -> tuple[dict, list[SourceConfig]]:
    with config_path.open("r", encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)

    run_settings = payload.get("run", {})
    sources = [
        SourceConfig(**source)
        for source in payload.get("sources", [])
        if source.get("enabled", False)
    ]
    return run_settings, sources


def collect_candidates(config_path: Path, run_date: str) -> list[CandidateReport]:
    run_settings, sources = load_sources(config_path)
    delay = float(run_settings.get("request_delay_seconds", 1.0))
    max_items = int(run_settings.get("max_items_per_source", 20))

    candidates: list[CandidateReport] = []
    for source in sources:
        if source.mode == "html_list":
            candidates.extend(_collect_from_html(source, run_date, max_items))
        elif source.mode == "api_list":
            candidates.extend(_collect_from_api_placeholder(source, run_date, max_items))
        time.sleep(delay)

    return candidates


def _collect_from_html(
    source: SourceConfig,
    run_date: str,
    max_items: int,
) -> list[CandidateReport]:
    response = requests.get(source.listing_url, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.select(source.link_selector or "a")
    candidates: list[CandidateReport] = []

    for index, link in enumerate(links[:max_items], start=1):
        href = link.get("href")
        if not href:
            continue

        title = link.get_text(" ", strip=True) or f"Untitled report {index:03d}"
        asset_id = f"ASSET_{index:03d}"
        candidates.append(
            CandidateReport(
                run_date=run_date,
                source_id=source.source_id,
                asset_id=asset_id,
                title=title,
                source_url=urljoin(source.listing_url, href),
            )
        )

    return candidates


def _collect_from_api_placeholder(
    source: SourceConfig,
    run_date: str,
    max_items: int,
) -> list[CandidateReport]:
    """Placeholder for private adapters.

    Public examples should not contain target-specific API shapes. Add private
    JSON parsing in a local adapter outside this repository.
    """
    _ = (source, run_date, max_items)
    return []


def download_candidates(
    candidates: list[CandidateReport],
    out_dir: Path,
    dry_run: bool = True,
) -> list[CandidateReport]:
    out_dir.mkdir(parents=True, exist_ok=True)

    for index, candidate in enumerate(candidates, start=1):
        filename = (
            f"{candidate.run_date}_{candidate.source_id}_"
            f"{candidate.asset_id}_{index:03d}.pdf"
        )
        target = out_dir / filename
        candidate.file_path = target

        if dry_run:
            continue

        response = requests.get(candidate.source_url, timeout=60)
        response.raise_for_status()
        target.write_bytes(response.content)

    return candidates


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
