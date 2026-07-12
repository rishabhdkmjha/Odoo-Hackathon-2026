from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import BookingStatusEnum


class Booking(Base):
    """
    Time-slot booking of a shared/bookable asset (room, vehicle, equipment).
    Overlap validation is enforced in the booking service, not the DB layer,
    to allow for clear, user-facing conflict messages.
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    booked_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False, index=True)
    purpose = Column(String(500), nullable=True)

    status = Column(Enum(BookingStatusEnum), nullable=False, default=BookingStatusEnum.UPCOMING, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    asset = relationship("Asset", back_populates="bookings")
    booked_by_user = relationship("User", back_populates="bookings", foreign_keys=[booked_by])
