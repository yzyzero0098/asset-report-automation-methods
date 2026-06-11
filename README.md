# Asset Report Automation Methods

Sanitized templates for reproducing a daily asset-report collection workflow.

This repository documents the method, folder layout, and reference code for an
automation pipeline that can:

- collect public report links from configurable sources
- download report files into date-based folders
- parse metadata from filenames and PDF text
- normalize records into a common schema
- reconcile duplicates before downstream upload or review
- run the same process as a scheduled daily job

The examples are intentionally generic. They do not include real source names,
issuer names, target URLs, login pages, account details, private endpoints, or
production data. Placeholder labels such as `SOURCE_A`, `ASSET_001`, and
`provider_slug` are used so the workflow can be studied without exposing the
original automation context.

## Repository Layout

```text
config/
  sources.example.yml       # placeholder source definitions
docs/
  sanitization_policy.md    # public-release rules
  workflow.md               # end-to-end pipeline notes
examples/
  sample_reports.csv        # synthetic normalized records
scripts/
  run_daily.ps1             # generic local scheduler entry point
src/asset_report_automation/
  cli.py                    # command-line interface
  fetch_reports.py          # generic collection skeleton
  models.py                 # shared dataclasses
  normalize.py              # normalization helpers
  parse_pdf.py              # PDF text extraction helpers
  reconcile.py              # duplicate and readiness checks
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

python -m asset_report_automation.cli fetch --config config\sources.example.yml --out data\raw
python -m asset_report_automation.cli parse --input data\raw --out data\parsed\records.csv
python -m asset_report_automation.cli reconcile --input data\parsed\records.csv --out data\ready\ready.csv
```

The default configuration is a template. Replace placeholder selectors and
endpoints only in a private working copy.

## Design Goals

- Keep collection, parsing, normalization, and upload preparation separate.
- Treat every source as a pluggable adapter.
- Save intermediate files for reproducibility.
- Keep public examples synthetic and source-neutral.
- Use dry-run checks before any downstream submission.

## What Is Not Included

- real source domains or page structures
- private credentials or session handling
- production scheduling metadata
- real report PDFs or crawled datasets
- real issuer, analyst, or provider names
