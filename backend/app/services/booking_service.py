"""
Resource Booking business logic (Screen 6).

Overlap rule: two bookings for the same asset overlap if
existing.start < new.end AND existing.end > new.start.
A request starting exactly when another ends (10:00-11:00 after a
9:00-10:00 booking) is allowed, matching the problem statement's example.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models.asset import Asset
from app.models.booking import Booking
from app.models.user import User
from app.models.enums import BookingStatusEnum, AssetStatusEnum
from app.schemas.booking_schema import BookingCreate, BookingUpdate
from app.services import audit_log_service, notification_service
from app.models.enums import NotificationTypeEnum
from app.utils.exceptions import NotFoundError, ConflictError, BadRequestError


ACTIVE_BOOKING_STATUSES = (BookingStatusEnum.UPCOMING, BookingStatusEnum.ONGOING)


def _has_overlap(db: Session, asset_id: int, start_time: datetime, end_time: datetime,
                  exclude_booking_id: Optional[int] = None) -> bool:
    query = db.query(Booking).filter(
        Booking.asset_id == asset_id,
        Booking.status.in_(ACTIVE_BOOKING_STATUSES),
        and_(Booking.start_time < end_time, Booking.end_time > start_time),
    )
    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)
    return db.query(query.exists()).scalar()


def list_bookings(db: Session, asset_id: Optional[int] = None, user_id: Optional[int] = None):
    query = db.query(Booking)
    if asset_id is not None:
        query = query.filter(Booking.asset_id == asset_id)
    if user_id is not None:
        query = query.filter(Booking.booked_by == user_id)
    return query.order_by(Booking.start_time).all()


def create_booking(db: Session, payload: BookingCreate, actor: User) -> Booking:
    asset = db.query(Asset).filter(Asset.id == payload.asset_id).first()
    if not asset:
        raise NotFoundError("Asset not found")
    if not asset.is_bookable:
        raise BadRequestError("This asset is not marked as a shared/bookable resource")
    if asset.status in (AssetStatusEnum.LOST, AssetStatusEnum.DISPOSED, AssetStatusEnum.MAINTENANCE):
        raise ConflictError(f"Asset is '{asset.status.value}' and cannot be booked")

    if _has_overlap(db, payload.asset_id, payload.start_time, payload.end_time):
        raise ConflictError(
            "This time slot overlaps with an existing booking for this resource"
        )

    booking = Booking(
        asset_id=payload.asset_id,
        booked_by=actor.id,
        department_id=payload.department_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        purpose=payload.purpose,
        status=BookingStatusEnum.UPCOMING,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    notification_service.create_notification(
        db,
        user_id=actor.id,
        type_=NotificationTypeEnum.BOOKING_CONFIRMED,
        message=f"Booking confirmed for '{asset.name}' from {payload.start_time} to {payload.end_time}.",
        related_entity_type="booking",
        related_entity_id=booking.id,
    )

    audit_log_service.log_action(
        db, user_id=actor.id, action="BOOKING_CREATED", entity_type="booking", entity_id=booking.id
    )
    return booking


def update_booking(db: Session, booking_id: int, payload: BookingUpdate, actor: User) -> Booking:
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise NotFoundError("Booking not found")

    new_start = payload.start_time or booking.start_time
    new_end = payload.end_time or booking.end_time

    if (payload.start_time or payload.end_time) and payload.status != BookingStatusEnum.CANCELLED:
        if new_end <= new_start:
            raise BadRequestError("end_time must be after start_time")
        if _has_overlap(db, booking.asset_id, new_start, new_end, exclude_booking_id=booking.id):
            raise ConflictError("This time slot overlaps with an existing booking for this resource")
        booking.start_time = new_start
        booking.end_time = new_end

    if payload.status is not None:
        booking.status = payload.status
        if payload.status == BookingStatusEnum.CANCELLED:
            notification_service.create_notification(
                db,
                user_id=booking.booked_by,
                type_=NotificationTypeEnum.BOOKING_CANCELLED,
                message=f"Your booking #{booking.id} has been cancelled.",
                related_entity_type="booking",
                related_entity_id=booking.id,
            )

    db.commit()
    db.refresh(booking)

    audit_log_service.log_action(
        db, user_id=actor.id, action="BOOKING_UPDATED", entity_type="booking", entity_id=booking.id
    )
    return booking
