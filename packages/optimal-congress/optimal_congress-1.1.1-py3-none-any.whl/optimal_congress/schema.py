"""Model definitions."""

from datetime import datetime
from typing import Annotated
from uuid import UUID

import pandera as pa
from pydantic import BaseModel, BeforeValidator, Field
from typing_extensions import Literal

from optimal_congress.config import HUB_EVENT_ROUTE

# languages to accept for events
EventLanguage = Literal["de", "en"]


class Room(BaseModel):
    """A room."""

    id: UUID
    name: str
    assembly: str

    class Config:
        frozen = True  # instances immutable and hashable


def parse_language(
    value: list[EventLanguage] | str | None,
) -> list[EventLanguage] | None:
    """Parse a language value to the expected list of languages.

    Args:
        value: The language value to parse.
    Returns:
        The parsed list of languages, or None.
    """
    match value:
        case None:
            return None
        case list():
            return value
        case str():
            return [i.strip() for i in value.split(",")]  # type: ignore


class Event(BaseModel):
    """An event."""

    id: UUID
    name: str
    slug: str
    track: str | None
    assembly: str
    room: UUID | None
    language: Annotated[
        list[EventLanguage] | None,
        BeforeValidator(parse_language),
    ] = Field(default=None)
    description: str
    schedule_start: datetime
    schedule_end: datetime

    def __hash__(self) -> int:
        """Events are equal, if they have same ID - regardless of other properties."""
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        """Events are equal, if they have same ID - regardless of other properties."""
        if not isinstance(other, Event):
            return NotImplemented
        return self.id == other.id

    def __str__(self) -> str:
        """Return a string representation of the event."""
        # get time without timezone
        timestamp_start = self.schedule_start.strftime("%Y-%m-%d %H:%M")
        time_end = self.schedule_end.strftime("%H:%M")
        return f"'{self.name}' ({timestamp_start} - {time_end}, {self.url})"

    @property
    def url(self) -> str:
        """Return the url of the event."""
        return f"{HUB_EVENT_ROUTE}/{self.slug}"


def events_overlap(event1: Event, event2: Event) -> bool:
    """Check if two events overlap."""
    return (
        event1.schedule_start < event2.schedule_end
        and event2.schedule_start < event1.schedule_end
    )


class Rating(BaseModel):
    """A rating for an event."""

    event_id: UUID
    score: float = Field(description="A positive number describing utility to attend.")
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        frozen = True  # instances immutable and hashable


class EventRating(BaseModel):
    """A container class for a rating and its associated event."""

    event: Event
    rating: Rating

    class Config:
        frozen = True  # instances immutable and hashable


class RatingsExport(pa.typing.DataFrame):
    """A schema for exporting and importing ratings to/from CSV."""

    score: float = pa.Field()
    name: str = pa.Field()
    url: str = pa.Field()
    id: UUID = pa.Field()
