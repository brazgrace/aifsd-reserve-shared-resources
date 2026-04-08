"""Pure booking rules: half-open intervals [start, end)."""

from __future__ import annotations

from datetime import datetime


def intervals_overlap(
    a_start: datetime,
    a_end: datetime,
    b_start: datetime,
    b_end: datetime,
) -> bool:
    """True if [a_start, a_end) and [b_start, b_end) share any instant."""
    return a_start < b_end and b_start < a_end


def ensure_valid_interval(start: datetime, end: datetime) -> None:
    if end <= start:
        msg = "end must be after start"
        raise ValueError(msg)
