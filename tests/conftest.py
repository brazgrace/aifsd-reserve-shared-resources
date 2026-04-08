"""Shared fixtures."""

import pytest
from httpx import ASGITransport, AsyncClient

from reserve_service.main import app, get_repository
from reserve_service.repository import InMemoryReservationRepository


@pytest.fixture
async def client() -> AsyncClient:
    repo = InMemoryReservationRepository()
    app.dependency_overrides[get_repository] = lambda: repo
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
