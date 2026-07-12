from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import MaintenanceStatusEnum, MaintenancePriorityEnum


class MaintenanceCreate(BaseModel):
    asset_id: int
    issue_description: str
    priority: MaintenancePriorityEnum = MaintenancePriorityEnum.MEDIUM
    photo_url: Optional[str] = None


class MaintenanceUpdate(BaseModel):
    """
    Used to drive the workflow: Pending -> Approved/Rejected -> Technician
    Assigned -> In Progress -> Resolved. Not every field is required per call.
    """

    status: Optional[MaintenanceStatusEnum] = None
    technician_name: Optional[str] = None
    resolution_notes: Optional[str] = None


class MaintenanceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    asset_id: int
    raised_by: int
    issue_description: str
    priority: MaintenancePriorityEnum
    photo_url: Optional[str] = None
    status: MaintenanceStatusEnum
    approved_by: Optional[int] = None
    technician_name: Optional[str] = None
    resolution_notes: Optional[str] = None
    created_at: datetime
    resolved_at: Optional[datetime] = None
