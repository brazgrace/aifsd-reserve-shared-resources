"""In-memory reservation repository."""

from datetime import UTC, datetime

import pytest

from reserve_service.repository import (
    Booked,
    Conflict,
    InMemoryReservationRepository,
    UnknownResource,
)


def utc(h: int, m: int = 0) -> datetime:
    return datetime(2026, 4, 8, h, m, tzinfo=UTC)


@pytest.fixture
def repo() -> InMemoryReservationRepository:
    return InMemoryReservationRepository()


@pytest.mark.asyncio
async def test_unknown_resource(repo: InMemoryReservationRepository) -> None:
    out = await repo.try_book("not-a-room", utc(9), utc(10))
    assert isinstance(out, UnknownResource)


@pytest.mark.asyncio
async def test_two_adjacent_bookings_succeed(
    repo: InMemoryReservationRepository,
) -> None:
    r1 = await repo.try_book("room-north", utc(9), utc(10))
    r2 = await repo.try_book("room-north", utc(10), utc(11))
    assert isinstance(r1, Booked)
    assert isinstance(r2, Booked)


@pytest.mark.asyncio
async def test_overlapping_second_booking_fails(
    repo: InMemoryReservationRepository,
) -> None:
    r1 = await repo.try_book("room-north", utc(9), utc(11))
    r2 = await repo.try_book("room-north", utc(10), utc(12))
    assert isinstance(r1, Booked)
    assert isinstance(r2, Conflict)


@pytest.mark.asyncio
async def test_same_resource_different_rooms_no_conflict(
    repo: InMemoryReservationRepository,
) -> None:
    r1 = await repo.try_book("room-north", utc(9), utc(10))
    r2 = await repo.try_book("room-south", utc(9), utc(10))
    assert isinstance(r1, Booked)
    assert isinstance(r2, Booked)
