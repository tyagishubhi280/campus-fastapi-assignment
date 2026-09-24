from enum import Enum

from pydantic import field_validator
from sqlmodel import Field, SQLModel


class ItemStatus(str, Enum):
    Lost = "Lost"
    Found = "Found"
    Returned = "Returned"


class EventStatus(str, Enum):
    Open = "Open"
    Closed = "Closed"


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: ItemStatus = Field(default=ItemStatus.Lost)

    @field_validator("title", "description", "category", "location", "reported_by")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field must contain meaningful text.")
        return value


class Event(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    venue: str
    capacity: int = Field(gt=0)
    organizer: str
    status: EventStatus = Field(default=EventStatus.Open)

    @field_validator("title", "venue", "organizer")
    @classmethod
    def validate_event_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field must contain meaningful text.")
        return value


class Reservation(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    event_id: int
    student_name: str
    roll_number: str
    email: str

    @field_validator("student_name", "roll_number")
    @classmethod
    def validate_reservation_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field must contain meaningful text.")
        return value
