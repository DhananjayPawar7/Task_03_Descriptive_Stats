"""Shared normalization rules for Task 03 scripts.

Pure Python analysis does NOT import this module so that it remains fully standard-library
and independent. Pandas/Polars use equivalent logic to keep results comparable.
"""
from __future__ import annotations

MISSING = {"", "na", "n/a", "null", "none", "nan", "missing", "-"}
PRIMARY_GROUP_CANDIDATES = [
    "page_id", "account_id", "user_id", "author_id", "page_name",
    "account_name", "username", "screen_name", "handle"
]
RECORD_ID_CANDIDATES = ["ad_id", "post_id", "tweet_id", "status_id", "message_id", "id"]


def auto_groups(columns: list[str]) -> list[list[str]]:
    """Pick sensible grouping keys from whatever schema is present."""
    colset = set(columns)
    groups: list[list[str]] = []
    primary = next((c for c in PRIMARY_GROUP_CANDIDATES if c in colset), None)
    record = next((c for c in RECORD_ID_CANDIDATES if c in colset), None)
    if primary:
        groups.append([primary])
    if primary and record and record != primary:
        groups.append([primary, record])
    elif record and not primary:
        groups.append([record])
    return groups
