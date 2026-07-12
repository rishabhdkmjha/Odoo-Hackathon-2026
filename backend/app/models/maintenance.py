from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import MaintenanceStatusEnum, MaintenancePriorityEnum


class MaintenanceRequest(Base):
    """
    Repair request workflow:
    Pending -> Approved/Rejected (Asset Manager) -> Technician Assigned -> In Progress -> Resolved.
    Asset flips to MAINTENANCE status on approval, back to AVAILABLE on resolution.
    """
    __tablename__ = "maintenance_requests"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False, index=True)
    raised_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    issue_description = Column(String(1000), nullable=False)
    priority = Column(Enum(MaintenancePriorityEnum), nullable=False, default=MaintenancePriorityEnum.MEDIUM)
    photo_url = Column(String(500), nullable=True)

    status = Column(
        Enum(MaintenanceStatusEnum), nullable=False, default=MaintenanceStatusEnum.PENDING, index=True
    )
    approved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    technician_name = Column(String(150), nullable=True)
    resolution_notes = Column(String(1000), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    resolved_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    asset = relationship("Asset", back_populates="maintenance_requests")
    raised_by_user = relationship("User", back_populates="maintenance_requests", foreign_keys=[raised_by])
