"""POST /book/{resource_id} contract."""

from datetime import UTC, datetime

import pytest
from httpx import AsyncClient


def payload(start_h: int, end_h: int) -> dict[str, str]:
    def iso(h: int) -> str:
        return datetime(2026, 4, 8, h, 0, tzinfo=UTC).isoformat().replace("+00:00", "Z")

    return {"start": iso(start_h), "end": iso(end_h)}


@pytest.mark.asyncio
async def test_book_created(client: AsyncClient) -> None:
    r = await client.post("/book/room-north", json=payload(9, 10))
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "booked"
    assert len(data["reservation_id"]) == 36


@pytest.mark.asyncio
async def test_unknown_resource_404(client: AsyncClient) -> None:
    r = await client.post("/book/unknown", json=payload(9, 10))
    assert r.status_code == 404
    assert r.json() == {"error": "unknown_resource"}


@pytest.mark.asyncio
async def test_overlap_409(client: AsyncClient) -> None:
    await client.post("/book/room-north", json=payload(9, 11))
    r = await client.post("/book/room-north", json=payload(10, 12))
    assert r.status_code == 409
    assert r.json() == {"error": "conflict"}


@pytest.mark.asyncio
async def test_end_before_start_422(client: AsyncClient) -> None:
    r = await client.post("/book/room-north", json=payload(11, 9))
    assert r.status_code == 422
