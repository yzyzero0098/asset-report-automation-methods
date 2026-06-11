from __future__ import annotations

import csv
from pathlib import Path


KEY_FIELDS = ("source_id", "asset_id", "report_date", "title", "file_hash")


def read_records(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_records(path: Path, records: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not records:
        path.write_text("", encoding="utf-8")
        return

    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)


def reconcile(records: list[dict[str, str]]) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    seen: set[tuple[str, ...]] = set()
    ready: list[dict[str, str]] = []
    rejected: list[dict[str, str]] = []

    for record in records:
        missing = [field for field in ("source_id", "asset_id", "report_date", "file_path") if not record.get(field)]
        if missing:
            record["status"] = "reject_missing_" + "_".join(missing)
            rejected.append(record)
            continue

        key = tuple(record.get(field, "").strip().lower() for field in KEY_FIELDS)
        if key in seen:
            record["status"] = "reject_duplicate"
            rejected.append(record)
            continue

        seen.add(key)
        record["status"] = "ready"
        ready.append(record)

    return ready, rejected
