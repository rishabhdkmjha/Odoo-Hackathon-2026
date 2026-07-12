from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.enums import AllocationStatusEnum


class AllocationCreate(BaseModel):
    asset_id: int
    employee_id: Optional[int] = None
    department_id: Optional[int] = None
    expected_return_date: Optional[date] = None

    @model_validator(mode="after")
    def check_target(self):
        if not self.employee_id and not self.department_id:
            raise ValueError("Either employee_id or department_id must be provided")
        return self


class AllocationReturn(BaseModel):
    allocation_id: int
    condition_checkin_notes: Optional[str] = None


class AllocationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_id: int
    employee_id: Optional[int] = None
    department_id: Optional[int] = None
    allocated_date: datetime
    expected_return_date: Optional[date] = None
    actual_return_date: Optional[datetime] = None
    status: AllocationStatusEnum
    condition_checkin_notes: Optional[str] = None


class TransferCreate(BaseModel):
    asset_id: int
    to_employee_id: int
    reason: Optional[str] = None


class TransferDecision(BaseModel):
    transfer_id: int
    approve: bool
    reason: Optional[str] = None


class TransferOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_id: int
    from_employee_id: Optional[int] = None
    to_employee_id: int
    requested_by: int
    approved_by: Optional[int] = None
    status: str
    reason: Optional[str] = None
    created_at: datetime
