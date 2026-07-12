from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_manager_or_head
from app.database.database import get_db
from app.models.user import User
from app.schemas.allocation_schema import TransferCreate, TransferDecision, TransferOut
from app.services import allocation_service
from app.utils.response import success_response

router = APIRouter(prefix="/transfer", tags=["Transfer"])


@router.post("")
def request_or_decide_transfer(
    payload: TransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Raises a transfer request for an asset that's already allocated to
    someone else. Requested -> Approved (by Asset Manager/Dept Head) -> Re-allocated.
    """
    transfer = allocation_service.request_transfer(db, payload, current_user)
    return success_response("Transfer request created successfully", TransferOut.model_validate(transfer).model_dump())


# Additive: decision endpoint for approving/rejecting a transfer request.
# Kept as a separate path so POST /transfer itself is untouched for the frontend.
@router.put("/decision")
def decide_transfer(
    payload: TransferDecision,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_manager_or_head),
):
    transfer = allocation_service.decide_transfer(db, payload, current_user)
    return success_response(
        f"Transfer {transfer.status} successfully", TransferOut.model_validate(transfer).model_dump()
    )
