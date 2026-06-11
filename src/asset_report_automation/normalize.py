from __future__ import annotations

import re
from datetime import datetime

from dateutil import parser


def normalize_asset_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value.strip()).strip("_")
    return cleaned.upper() or "ASSET_UNKNOWN"


def normalize_source_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "_", value.strip()).strip("_")
    return cleaned.upper() or "SOURCE_UNKNOWN"


def normalize_title(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def normalize_date(value: str | None, fallback: str) -> str:
    if not value:
        return fallback

    try:
        return parser.parse(value).strftime("%Y-%m-%d")
    except (TypeError, ValueError, parser.ParserError):
        return fallback


def today_label(now: datetime | None = None) -> str:
    return (now or datetime.now()).strftime("%Y%m%d")
