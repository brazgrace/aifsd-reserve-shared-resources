# Reservation service of shared resources

Small **FastAPI** service for booking **shared resources** (meeting rooms): one endpoint, in-memory storage, no authentication.

## Setup

Requires **Python 3.11+** and [Poetry](https://python-poetry.org/).

```bash
poetry install
```

## Run

```bash
poetry run uvicorn reserve_service.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for the interactive OpenAPI UI.

## API

### `POST /book/{resource_id}`

Books the interval `[start, end)` (half-open: the instant `end` is free for the next booking).

**Body** (JSON, timezone-aware ISO-8601 datetimes):

```json
{
  "start": "2026-04-08T14:00:00Z",
  "end": "2026-04-08T15:00:00Z"
}
```

**Responses**


| Status | Meaning                                                                |
| ------ | ---------------------------------------------------------------------- |
| `201`  | `{"status":"booked","reservation_id":"<uuid>"}`                        |
| `404`  | `{"error":"unknown_resource"}` — `resource_id` not in the catalog      |
| `409`  | `{"error":"conflict"}` — overlaps an existing booking on that resource |
| `422`  | Validation error (e.g. `end` not after `start`, naive datetime)        |


**Valid `resource_id` values** (pre-registered in code): `room-north`, `room-south`.

## Tests and checks

```bash
poetry run pytest
poetry run ruff check src tests
poetry run mypy src
```

## Notes

- State is **in-memory**; restarting the process clears reservations.
- **Concurrency** within one process is serialized with an `asyncio` lock; multiple workers or hosts would need shared storage and transactions.
- **Auth** is intentionally out of scope.

