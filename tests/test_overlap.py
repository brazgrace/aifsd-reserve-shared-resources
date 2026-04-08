"""Half-open interval overlap and validation."""

from datetime import UTC, datetime

import pytest

from reserve_service.domain import ensure_valid_interval, intervals_overlap


def dt(h: int, m: int = 0) -> datetime:
    return datetime(2026, 4, 8, h, m, tzinfo=UTC)


@pytest.mark.parametrize(
    ("a", "b", "expect_overlap"),
    [
        # disjoint
        ((dt(9), dt(10)), (dt(11), dt(12)), False),
        # adjacent: first ends when second starts — no overlap ([start, end) half-open)
        ((dt(9), dt(10)), (dt(10), dt(11)), False),
        ((dt(10), dt(11)), (dt(9), dt(10)), False),
        # partial overlap
        ((dt(9), dt(11)), (dt(10), dt(12)), True),
        # containment
        ((dt(8), dt(14)), (dt(10), dt(11)), True),
        ((dt(10), dt(11)), (dt(8), dt(14)), True),
    ],
)
def test_intervals_overlap(
    a: tuple[datetime, datetime],
    b: tuple[datetime, datetime],
    expect_overlap: bool,
) -> None:
    assert intervals_overlap(a[0], a[1], b[0], b[1]) is expect_overlap


def test_ensure_valid_interval_rejects_non_positive_length() -> None:
    with pytest.raises(ValueError, match="end must be after start"):
        ensure_valid_interval(dt(10), dt(10))
    with pytest.raises(ValueError, match="end must be after start"):
        ensure_valid_interval(dt(11), dt(10))
