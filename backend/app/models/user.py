from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import RoleEnum, UserStatusEnum


class User(Base):
    """
    Represents every person in the system: Admin, Asset Manager,
    Department Head, or Employee. Everyone signs up as an Employee;
    roles are only elevated by an Admin via the Employee Directory.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    role = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.EMPLOYEE)
    status = Column(Enum(UserStatusEnum), nullable=False, default=UserStatusEnum.ACTIVE)

    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    department = relationship(
        "Department",
        back_populates="employees",
        foreign_keys=[department_id],
    )
    headed_department = relationship(
        "Department",
        back_populates="head",
        foreign_keys="Department.head_id",
        uselist=False,
    )
    allocations = relationship(
        "AssetAllocation",
        back_populates="employee",
        foreign_keys="AssetAllocation.employee_id",
    )
    bookings = relationship("Booking", back_populates="booked_by_user", foreign_keys="Booking.booked_by")
    maintenance_requests = relationship(
        "MaintenanceRequest", back_populates="raised_by_user", foreign_keys="MaintenanceRequest.raised_by"
    )
    notifications = relationship("Notification", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")
