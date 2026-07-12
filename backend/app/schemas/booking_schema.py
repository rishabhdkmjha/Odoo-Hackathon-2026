from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

from app.models.enums import BookingStatusEnum


class BookingCreate(BaseModel):
    asset_id: int
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None
    department_id: Optional[int] = None

    @model_validator(mode="after")
    def validate_times(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class BookingUpdate(BaseModel):
    status: Optional[BookingStatusEnum] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class BookingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_id: int
    booked_by: int
    department_id: Optional[int] = None
    start_time: datetime
    end_time: datetime
    purpose: Optional[str] = None
    status: BookingStatusEnum
    created_at: datetime
