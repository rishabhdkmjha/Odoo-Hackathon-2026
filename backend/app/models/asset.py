from sqlalchemy import Column, Integer, String, Float, Boolean, Enum, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import AssetStatusEnum, AssetConditionEnum


class Asset(Base):
    """
    Core asset record. asset_tag is auto-generated (e.g. AF-0001).
    is_bookable marks it as a shared/bookable resource (room, vehicle, equipment).
    """
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    asset_tag = Column(String(50), nullable=False, unique=True, index=True)
    serial_number = Column(String(150), nullable=True, index=True)
    qr_code = Column(String(150), nullable=True, unique=True)

    category_id = Column(Integer, ForeignKey("asset_categories.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)

    acquisition_date = Column(Date, nullable=True)
    acquisition_cost = Column(Float, nullable=True)  # reporting/ranking only, not linked to accounting

    condition = Column(Enum(AssetConditionEnum), nullable=False, default=AssetConditionEnum.NEW)
    location = Column(String(200), nullable=True)
    status = Column(Enum(AssetStatusEnum), nullable=False, default=AssetStatusEnum.AVAILABLE, index=True)

    is_bookable = Column(Boolean, default=False, nullable=False)
    photo_url = Column(String(500), nullable=True)
    document_url = Column(String(500), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    category = relationship("AssetCategory", back_populates="assets")
    department = relationship("Department", back_populates="assets")
    allocations = relationship("AssetAllocation", back_populates="asset", cascade="all, delete-orphan")
    transfer_requests = relationship("TransferRequest", back_populates="asset", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="asset", cascade="all, delete-orphan")
    maintenance_requests = relationship(
        "MaintenanceRequest", back_populates="asset", cascade="all, delete-orphan"
    )
