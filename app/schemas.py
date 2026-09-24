from pydantic import EmailStr, Field, field_validator
from sqlmodel import SQLModel

from .models import EventStatus, ItemStatus


class ItemCreate(SQLModel):
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: ItemStatus

    @field_validator("title", "description", "category", "location", "reported_by")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field must contain meaningful text.")
        return value


class ItemUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    location: str | None = None
    reported_by: str | None = None
    status: ItemStatus | None = None

    @field_validator("title", "description", "category", "location", "reported_by")
    @classmethod
    def validate_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("This field must contain meaningful text.")
        return value


class EventCreate(SQLModel):
    title: str
    venue: str
    capacity: int = Field(gt=0)
    organizer: str
    status: EventStatus = EventStatus.Open

    @field_validator("title", "venue", "organizer")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field must contain meaningful text.")
        return value


class EventUpdate(SQLModel):
    title: str | None = None
    venue: str | None = None
    capacity: int | None = Field(default=None, gt=0)
    organizer: str | None = None
    status: EventStatus | None = None

    @field_validator("title", "venue", "organizer")
    @classmethod
    def validate_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("This field must contain meaningful text.")
        return value


class ReservationCreate(SQLModel):
    student_name: str
    roll_number: str
    email: EmailStr

    @field_validator("student_name", "roll_number")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("This field must contain meaningful text.")
        return value
