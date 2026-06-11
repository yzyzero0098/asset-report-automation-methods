param(
    [string]$RepoRoot = (Resolve-Path "$PSScriptRoot\..").Path,
    [string]$RunDate = (Get-Date -Format "yyyyMMdd"),
    [switch]$Download
)

$ErrorActionPreference = "Stop"

$python = Join-Path $RepoRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

$config = Join-Path $RepoRoot "config\sources.example.yml"
$rawDir = Join-Path $RepoRoot "data\raw\$RunDate"
$parsedCsv = Join-Path $RepoRoot "data\parsed\$RunDate\records.csv"
$readyCsv = Join-Path $RepoRoot "data\ready\$RunDate\ready.csv"
$rejectCsv = Join-Path $RepoRoot "data\ready\$RunDate\rejects.csv"

$fetchArgs = @(
    "-m", "asset_report_automation.cli",
    "fetch",
    "--config", $config,
    "--out", $rawDir,
    "--run-date", $RunDate
)

if ($Download) {
    $fetchArgs += "--download"
}

Push-Location $RepoRoot
try {
    & $python @fetchArgs
    & $python -m asset_report_automation.cli parse --input $rawDir --out $parsedCsv
    & $python -m asset_report_automation.cli reconcile --input $parsedCsv --out $readyCsv --rejects $rejectCsv
    & $python -m asset_report_automation.cli dry-run --input $readyCsv
}
finally {
    Pop-Location
}
