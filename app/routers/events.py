from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ..database import get_session
from ..models import Event, EventStatus, Reservation
from ..schemas import EventCreate, EventUpdate, ReservationCreate

router = APIRouter(tags=["Task 2 - Events & Reservations"])


@router.post("/events", response_model=Event, status_code=status.HTTP_201_CREATED)
def create_event(
    event_data: EventCreate,
    session: Session = Depends(get_session),
):
    event = Event(**event_data.model_dump())
    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.get("/events", response_model=list[Event])
def get_events(session: Session = Depends(get_session)):
    return session.exec(select(Event)).all()


@router.get("/events/{event_id}", response_model=Event)
def get_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )
    return event


@router.put("/events/{event_id}", response_model=Event)
def update_event(
    event_id: int,
    event_data: EventUpdate,
    session: Session = Depends(get_session),
):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    update_data = event_data.model_dump(exclude_unset=True)

    # Do not allow the event capacity to be reduced below existing bookings.
    if "capacity" in update_data:
        booked = len(
            session.exec(
                select(Reservation).where(Reservation.event_id == event_id)
            ).all()
        )
        if update_data["capacity"] < booked:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Capacity cannot be less than current bookings ({booked}).",
            )

    for key, value in update_data.items():
        setattr(event, key, value)

    session.add(event)
    session.commit()
    session.refresh(event)
    return event


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, session: Session = Depends(get_session)):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    # Remove reservations first so no orphan reservation records remain.
    reservations = session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all()
    for reservation in reservations:
        session.delete(reservation)

    session.delete(event)
    session.commit()
    return None


@router.post(
    "/events/{event_id}/reserve",
    response_model=Reservation,
    status_code=status.HTTP_201_CREATED,
)
def create_reservation(
    event_id: int,
    reservation_data: ReservationCreate,
    session: Session = Depends(get_session),
):
    # 1. Verify that the event exists.
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    # 2. Verify that the event is open.
    if event.status != EventStatus.Open:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reservations are closed for this event.",
        )

    # 3. Count current reservations.
    booked = len(
        session.exec(
            select(Reservation).where(Reservation.event_id == event_id)
        ).all()
    )

    # 4. Prevent overbooking.
    if booked >= event.capacity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Event is full. No more reservations are allowed.",
        )

    reservation = Reservation(
        event_id=event_id,
        student_name=reservation_data.student_name,
        roll_number=reservation_data.roll_number,
        email=str(reservation_data.email),
    )
    session.add(reservation)
    session.commit()
    session.refresh(reservation)
    return reservation


@router.get(
    "/events/{event_id}/reservations",
    response_model=list[Reservation],
)
def get_event_reservations(
    event_id: int,
    session: Session = Depends(get_session),
):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    return session.exec(
        select(Reservation).where(Reservation.event_id == event_id)
    ).all()


@router.delete(
    "/reservations/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def cancel_reservation(
    reservation_id: int,
    session: Session = Depends(get_session),
):
    reservation = session.get(Reservation, reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found",
        )

    session.delete(reservation)
    session.commit()
    return None


@router.get("/events/{event_id}/availability")
def get_availability(
    event_id: int,
    session: Session = Depends(get_session),
):
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    booked = len(
        session.exec(
            select(Reservation).where(Reservation.event_id == event_id)
        ).all()
    )

    return {
        "capacity": event.capacity,
        "booked": booked,
        "remaining": event.capacity - booked,
    }
