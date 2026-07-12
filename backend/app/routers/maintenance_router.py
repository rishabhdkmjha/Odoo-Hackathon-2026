from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.maintenance_schema import MaintenanceCreate, MaintenanceUpdate, MaintenanceOut
from app.services import maintenance_service
from app.utils.response import success_response

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.get("")
def list_maintenance_requests(
    asset_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    requests = maintenance_service.list_maintenance_requests(db, asset_id, status)
    return success_response(
        "Maintenance requests fetched successfully",
        [MaintenanceOut.model_validate(r).model_dump() for r in requests],
    )


@router.post("")
def raise_maintenance_request(
    payload: MaintenanceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Raise a request: select asset, describe issue, set priority, attach photo."""
    request = maintenance_service.create_maintenance_request(db, payload, current_user)
    return success_response(
        "Maintenance request raised successfully", MaintenanceOut.model_validate(request).model_dump()
    )


# Additive: drives the workflow (approve/reject/assign technician/resolve).
@router.put("/{request_id}")
def update_maintenance_request(
    request_id: int,
    payload: MaintenanceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    request = maintenance_service.update_maintenance_request(db, request_id, payload, current_user)
    return success_response(
        "Maintenance request updated successfully", MaintenanceOut.model_validate(request).model_dump()
    )
