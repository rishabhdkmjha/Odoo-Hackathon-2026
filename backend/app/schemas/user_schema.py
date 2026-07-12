from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from app.models.enums import RoleEnum, UserStatusEnum


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    status: UserStatusEnum
    department_id: Optional[int] = None
    created_at: datetime


class EmployeeCreate(BaseModel):
    """Used by Admin to directly create an employee record (Organization Setup -> Employee Directory)."""

    name: str = Field(..., min_length=2, max_length=150)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    department_id: Optional[int] = None
    role: RoleEnum = RoleEnum.EMPLOYEE


class EmployeeUpdate(BaseModel):
    """
    Admin-only update. This is the ONLY place role can be changed
    (promotion to Department Head / Asset Manager).
    """

    name: Optional[str] = Field(None, min_length=2, max_length=150)
    department_id: Optional[int] = None
    role: Optional[RoleEnum] = None
    status: Optional[UserStatusEnum] = None
