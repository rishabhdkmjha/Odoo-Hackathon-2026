from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import require_manager_or_head, get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.allocation_schema import AllocationCreate, AllocationOut, AllocationReturn
from app.services import allocation_service
from app.utils.response import success_response

router = APIRouter(prefix="/allocation", tags=["Allocation"])


@router.post("")
def allocate_asset(
    payload: AllocationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager_or_head),
):
    """
    Allocates an asset to an employee/department.
    Blocked with a 409 if the asset already has an active allocation -
    the frontend should surface the 'Transfer Request' action in that case
    (see POST /transfer).
    """
    result = allocation_service.allocate_asset(db, payload, current_user)
    return success_response(
        "Asset allocated successfully", AllocationOut.model_validate(result["allocation"]).model_dump()
    )


# --- Additive endpoints (not in the original frontend contract, but required
# by the "Return flow" and "Overdue allocations" features). Safe additions:
# they don't rename or replace any endpoint the frontend already depends on.

@router.put("/return")
def return_asset(
    payload: AllocationReturn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager_or_head),
):
    """Marks an active allocation as returned, capturing condition check-in notes."""
    allocation = allocation_service.return_asset(db, payload, current_user)
    return success_response("Asset returned successfully", AllocationOut.model_validate(allocation).model_dump())


@router.get("/overdue")
def get_overdue_allocations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Allocations past their Expected Return Date, for the Dashboard + Notifications feed."""
    overdue = allocation_service.list_overdue_allocations(db)
    return success_response(
        "Overdue allocations fetched successfully",
        [AllocationOut.model_validate(a).model_dump() for a in overdue],
    )
