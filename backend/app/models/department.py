from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database import Base
from app.models.enums import DepartmentStatusEnum


class Department(Base):
    """
    Organizational unit. Supports an optional parent department for hierarchy
    and an optional Department Head (a User with role=department_head).
    """
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False, unique=True)
    head_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    parent_department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    status = Column(Enum(DepartmentStatusEnum), nullable=False, default=DepartmentStatusEnum.ACTIVE)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    head = relationship("User", back_populates="headed_department", foreign_keys=[head_id])
    employees = relationship("User", back_populates="department", foreign_keys="User.department_id")
    parent = relationship("Department", remote_side=[id], backref="sub_departments")
    assets = relationship("Asset", back_populates="department")
    allocations = relationship("AssetAllocation", back_populates="department")
