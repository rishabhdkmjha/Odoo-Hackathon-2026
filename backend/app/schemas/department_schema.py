from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from app.models.enums import DepartmentStatusEnum


class DepartmentCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    head_id: Optional[int] = None
    parent_department_id: Optional[int] = None
    status: DepartmentStatusEnum = DepartmentStatusEnum.ACTIVE


class DepartmentUpdate(BaseModel):
    name: Optional[str] = None
    head_id: Optional[int] = None
    parent_department_id: Optional[int] = None
    status: Optional[DepartmentStatusEnum] = None


class DepartmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    head_id: Optional[int] = None
    parent_department_id: Optional[int] = None
    status: DepartmentStatusEnum
    created_at: datetime
