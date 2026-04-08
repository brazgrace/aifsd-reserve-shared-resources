"""HTTP request/response models."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator


class BookRequest(BaseModel):
    start: datetime = Field(
        ...,
        description="Interval start (timezone-aware, ISO-8601).",
    )
    end: datetime = Field(
        ...,
        description="Interval end (exclusive in domain rules).",
    )

    @model_validator(mode="after")
    def end_after_start(self) -> BookRequest:
        if self.end <= self.start:
            msg = "end must be after start"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def require_timezone_aware(self) -> BookRequest:
        if self.start.tzinfo is None or self.end.tzinfo is None:
            msg = "start and end must be timezone-aware datetimes"
            raise ValueError(msg)
        return self


class BookedResponse(BaseModel):
    status: Literal["booked"] = "booked"
    reservation_id: str
