# Workflow

The automation is split into small stages so each step can be reproduced and
audited independently.

## 1. Date Folder

Create a run folder with a stable date label:

```text
data/
  raw/YYYYMMDD/
  parsed/YYYYMMDD/
  ready/YYYYMMDD/
  logs/YYYYMMDD/
```

This makes daily reruns easy to compare.

## 2. Source Collection

Each source adapter receives:

- a public listing endpoint or search page
- selector rules for report links
- optional pagination settings
- a delay policy
- a maximum item count

The adapter returns candidate report links without parsing business metadata.

## 3. File Download

Downloaded files are stored with neutral names:

```text
YYYYMMDD_SOURCE_A_ASSET_001_001.pdf
YYYYMMDD_SOURCE_B_ASSET_002_001.pdf
```

The original URL is stored in metadata, not in the filename.

## 4. Metadata Parsing

The parser extracts:

- report date
- source id
- asset id
- title
- author label
- rating or opinion text
- current value
- target value
- file hash

Fields that cannot be extracted are left blank and reviewed later.

## 5. Normalization

Records are converted into a common schema:

```text
run_date, source_id, asset_id, report_date, title, author_label,
opinion, current_value, target_value, file_path, file_hash, source_url
```

## 6. Reconciliation

Duplicate records are grouped by:

- normalized asset id
- report date
- normalized title
- source id
- file hash

The output is a ready table plus a reject table for manual review.

## 7. Dry Run

Before downstream submission, validate:

- required fields are present
- PDFs exist
- duplicate count is acceptable
- source URLs are syntactically valid
- no private labels appear in output

## 8. Scheduling

Use the PowerShell wrapper in `scripts/run_daily.ps1` from Task Scheduler or
another local scheduler. Keep environment-specific paths outside the public
repository.
