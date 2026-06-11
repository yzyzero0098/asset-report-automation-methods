from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SourceConfig:
    source_id: str
    provider_slug: str
    enabled: bool
    mode: str
    listing_url: str
    link_selector: str | None = None
    title_selector: str | None = None
    date_selector: str | None = None
    link_json_path: str | None = None
    title_json_path: str | None = None
    date_json_path: str | None = None


@dataclass
class CandidateReport:
    run_date: str
    source_id: str
    asset_id: str
    title: str
    source_url: str
    report_date: str | None = None
    file_path: Path | None = None


@dataclass
class ReportRecord:
    run_date: str
    source_id: str
    asset_id: str
    report_date: str
    title: str
    author_label: str
    opinion: str
    current_value: str
    target_value: str
    file_path: str
    file_hash: str
    source_url: str
    status: str = "ready"
