from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.booking_schema import BookingCreate, BookingUpdate, BookingOut
from app.services import booking_service
from app.utils.response import success_response

router = APIRouter(prefix="/booking", tags=["Booking"])


@router.get("")
def list_bookings(
    asset_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Calendar view of a resource's existing bookings."""
    bookings = booking_service.list_bookings(db, asset_id=asset_id)
    return success_response(
        "Bookings fetched successfully", [BookingOut.model_validate(b).model_dump() for b in bookings]
    )


@router.post("")
def create_booking(
    payload: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """
    Books a shared resource by time slot. Rejects overlapping requests
    with a 409 (e.g. Room B2 booked 9:00-10:00 blocks a 9:30-10:30 request,
    but allows a 10:00-11:00 request).
    """
    booking = booking_service.create_booking(db, payload, current_user)
    return success_response("Booking created successfully", BookingOut.model_validate(booking).model_dump())


# Additive: cancel/reschedule endpoint for an existing booking.
@router.put("/{booking_id}")
def update_booking(
    booking_id: int,
    payload: BookingUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    booking = booking_service.update_booking(db, booking_id, payload, current_user)
    return success_response("Booking updated successfully", BookingOut.model_validate(booking).model_dump())
