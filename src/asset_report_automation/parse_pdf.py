from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

from .fetch_reports import file_hash
from .models import ReportRecord
from .normalize import normalize_date, normalize_title


def extract_text(path: Path, max_pages: int = 3) -> str:
    reader = PdfReader(str(path))
    chunks: list[str] = []
    for page in reader.pages[:max_pages]:
        chunks.append(page.extract_text() or "")
    return "\n".join(chunks)


def parse_report_file(
    path: Path,
    run_date: str,
    source_id: str,
    asset_id: str,
    source_url: str,
) -> ReportRecord:
    text = extract_text(path)
    title = _first_nonempty_line(text) or path.stem

    return ReportRecord(
        run_date=run_date,
        source_id=source_id,
        asset_id=asset_id,
        report_date=normalize_date(_find_date(text), run_date),
        title=normalize_title(title),
        author_label=_find_author_label(text),
        opinion=_find_opinion(text),
        current_value=_find_labeled_number(text, "current"),
        target_value=_find_labeled_number(text, "target"),
        file_path=str(path),
        file_hash=file_hash(path),
        source_url=source_url,
    )


def _first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        if line.strip():
            return line.strip()
    return ""


def _find_date(text: str) -> str | None:
    match = re.search(r"\b(20\d{2})[-./](\d{1,2})[-./](\d{1,2})\b", text)
    return match.group(0) if match else None


def _find_author_label(text: str) -> str:
    match = re.search(r"\bAUTHOR[_ -]?(\d{1,3})\b", text, re.IGNORECASE)
    if not match:
        return ""
    return f"AUTHOR_{int(match.group(1)):02d}"


def _find_opinion(text: str) -> str:
    lowered = text.lower()
    for label in ("positive", "neutral", "negative"):
        if label in lowered:
            return label
    return ""


def _find_labeled_number(text: str, label: str) -> str:
    pattern = rf"{label}\s*(?:value)?\s*[:=]\s*([0-9,]+(?:\.\d+)?)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).replace(",", "") if match else ""
