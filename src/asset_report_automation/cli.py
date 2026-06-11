from __future__ import annotations

import argparse
import csv
from pathlib import Path

from .fetch_reports import collect_candidates, download_candidates
from .normalize import today_label
from .reconcile import read_records, reconcile, write_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Sanitized asset-report automation")
    subparsers = parser.add_subparsers(dest="command", required=True)

    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("--config", required=True, type=Path)
    fetch_parser.add_argument("--out", required=True, type=Path)
    fetch_parser.add_argument("--run-date", default=today_label())
    fetch_parser.add_argument("--download", action="store_true")

    parse_parser = subparsers.add_parser("parse")
    parse_parser.add_argument("--input", required=True, type=Path)
    parse_parser.add_argument("--out", required=True, type=Path)

    reconcile_parser = subparsers.add_parser("reconcile")
    reconcile_parser.add_argument("--input", required=True, type=Path)
    reconcile_parser.add_argument("--out", required=True, type=Path)
    reconcile_parser.add_argument("--rejects", type=Path)

    dry_run_parser = subparsers.add_parser("dry-run")
    dry_run_parser.add_argument("--input", required=True, type=Path)

    args = parser.parse_args()

    if args.command == "fetch":
        candidates = collect_candidates(args.config, args.run_date)
        candidates = download_candidates(candidates, args.out, dry_run=not args.download)
        _write_candidates(args.out / "candidates.csv", candidates)
    elif args.command == "parse":
        _write_parse_placeholder(args.input, args.out)
    elif args.command == "reconcile":
        records = read_records(args.input)
        ready, rejected = reconcile(records)
        write_records(args.out, ready)
        if args.rejects:
            write_records(args.rejects, rejected)
    elif args.command == "dry-run":
        records = read_records(args.input)
        ready, rejected = reconcile(records)
        print(f"ready={len(ready)} rejected={len(rejected)}")


def _write_candidates(path: Path, candidates: list) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["run_date", "source_id", "asset_id", "title", "source_url", "report_date", "file_path"],
        )
        writer.writeheader()
        for candidate in candidates:
            writer.writerow(
                {
                    "run_date": candidate.run_date,
                    "source_id": candidate.source_id,
                    "asset_id": candidate.asset_id,
                    "title": candidate.title,
                    "source_url": candidate.source_url,
                    "report_date": candidate.report_date or "",
                    "file_path": str(candidate.file_path or ""),
                }
            )


def _write_parse_placeholder(input_dir: Path, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        "run_date,source_id,asset_id,report_date,title,author_label,opinion,"
        "current_value,target_value,file_path,file_hash,source_url,status\n",
        encoding="utf-8",
    )
    print(f"Parse placeholder wrote schema to {out_path}. Input directory was {input_dir}.")


if __name__ == "__main__":
    main()
