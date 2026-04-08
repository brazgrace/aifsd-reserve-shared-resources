"""Thread-safe in-memory reservations (single process)."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime
from typing import Final
from uuid import uuid4

from reserve_service.domain import ensure_valid_interval, intervals_overlap

# Pre-registered resources (no CRUD in this service).
KNOWN_RESOURCES: Final[frozenset[str]] = frozenset({"room-north", "room-south"})


@dataclass(frozen=True, slots=True)
class Booked:
    reservation_id: str


@dataclass(frozen=True, slots=True)
class Conflict:
    """Another reservation on this resource overlaps the requested interval."""


@dataclass(frozen=True, slots=True)
class UnknownResource:
    """resource_id is not in the known catalog."""


BookOutcome = Booked | Conflict | UnknownResource


@dataclass(slots=True)
class _Reservation:
    resource_id: str
    start: datetime
    end: datetime
    reservation_id: str


class InMemoryReservationRepository:
    """Serializes try_book with a lock so concurrent requests cannot double-book."""

    def __init__(self, known: frozenset[str] | None = None) -> None:
        self._known = known if known is not None else KNOWN_RESOURCES
        self._rows: list[_Reservation] = []
        self._lock = asyncio.Lock()

    async def try_book(
        self,
        resource_id: str,
        start: datetime,
        end: datetime,
    ) -> BookOutcome:
        ensure_valid_interval(start, end)
        if resource_id not in self._known:
            return UnknownResource()

        async with self._lock:
            for existing in self._rows:
                if existing.resource_id != resource_id:
                    continue
                if intervals_overlap(start, end, existing.start, existing.end):
                    return Conflict()

            rid = str(uuid4())
            self._rows.append(
                _Reservation(resource_id, start, end, rid),
            )
            return Booked(reservation_id=rid)
