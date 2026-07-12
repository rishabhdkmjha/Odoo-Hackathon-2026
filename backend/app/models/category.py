from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base


class AssetCategory(Base):
    """
    Category grouping for assets (Electronics, Furniture, Vehicles, etc.)
    extra_fields stores optional category-specific metadata schema,
    e.g. {"warranty_period_months": 24} as free-form JSON.
    """
    __tablename__ = "asset_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    description = Column(String(500), nullable=True)
    extra_fields = Column(JSON, nullable=True, default=dict)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    assets = relationship("Asset", back_populates="category")
