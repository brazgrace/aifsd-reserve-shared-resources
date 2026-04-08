"""FastAPI app: single booking endpoint."""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from reserve_service.repository import (
    Booked,
    Conflict,
    InMemoryReservationRepository,
    UnknownResource,
)
from reserve_service.schemas import BookedResponse, BookRequest

app = FastAPI(title="Reserve Service", version="0.1.0")

_repository = InMemoryReservationRepository()


def get_repository() -> InMemoryReservationRepository:
    return _repository


@app.post(
    "/book/{resource_id}",
    response_model=BookedResponse,
    status_code=201,
    responses={
        404: {"model": None, "description": "Unknown resource"},
        409: {"model": None, "description": "Overlapping reservation"},
    },
)
async def book_resource(
    resource_id: str,
    body: BookRequest,
    repo: Annotated[InMemoryReservationRepository, Depends(get_repository)],
) -> BookedResponse | JSONResponse:
    outcome = await repo.try_book(resource_id, body.start, body.end)
    if isinstance(outcome, Booked):
        return BookedResponse(reservation_id=outcome.reservation_id)
    if isinstance(outcome, UnknownResource):
        return JSONResponse(status_code=404, content={"error": "unknown_resource"})
    if isinstance(outcome, Conflict):
        return JSONResponse(status_code=409, content={"error": "conflict"})
    raise AssertionError("unreachable")
