from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import AllocationStatusEnum


class AssetAllocation(Base):
    """
    Tracks who currently (or historically) holds an asset.
    Only one ACTIVE allocation per asset is allowed at a time - this is the
    core "no double allocation" invariant, enforced in the allocation service.
    """
    __tablename__ = "asset_allocations"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    allocated_date = Column(DateTime(timezone=True), server_default=func.now())
    expected_return_date = Column(Date, nullable=True)
    actual_return_date = Column(DateTime(timezone=True), nullable=True)

    status = Column(Enum(AllocationStatusEnum), nullable=False, default=AllocationStatusEnum.ACTIVE, index=True)
    condition_checkin_notes = Column(String(1000), nullable=True)

    allocated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    asset = relationship("Asset", back_populates="allocations")
    employee = relationship("User", back_populates="allocations", foreign_keys=[employee_id])
    department = relationship("Department", back_populates="allocations")


class TransferRequest(Base):
    """
    Transfer workflow: Requested -> Approved (by Asset Manager/Dept Head) -> Re-allocated.
    Created when an employee tries to claim an already-allocated asset,
    or explicitly initiates a transfer/return.
    """
    __tablename__ = "transfer_requests"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)

    from_employee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    to_employee_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    requested_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    status = Column(String(20), nullable=False, default="requested")  # requested/approved/rejected
    reason = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    asset = relationship("Asset", back_populates="transfer_requests")
