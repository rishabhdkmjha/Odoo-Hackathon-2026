"""
Allocation & Transfer business logic (Screen 5).

Core rule: an asset can have at most one ACTIVE allocation at a time.
Trying to allocate an already-held asset is blocked and the caller is
offered a transfer request instead - mirroring the Priya/Raj example
in the problem statement.
"""
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.allocation import AssetAllocation, TransferRequest
from app.models.user import User
from app.models.enums import AllocationStatusEnum, AssetStatusEnum, NotificationTypeEnum
from app.schemas.allocation_schema import AllocationCreate, AllocationReturn, TransferCreate, TransferDecision
from app.services import audit_log_service, notification_service
from app.services.asset_service import get_asset_or_404, transition_status
from app.utils.exceptions import NotFoundError, ConflictError, BadRequestError, ForbiddenError


def _get_active_allocation(db: Session, asset_id: int) -> AssetAllocation | None:
    return (
        db.query(AssetAllocation)
        .filter(AssetAllocation.asset_id == asset_id, AssetAllocation.status == AllocationStatusEnum.ACTIVE)
        .first()
    )


def allocate_asset(db: Session, payload: AllocationCreate, actor: User) -> dict:
    asset = get_asset_or_404(db, payload.asset_id)

    active_allocation = _get_active_allocation(db, asset.id)
    if active_allocation is not None:
        # Blocked: asset already held. Tell the caller who holds it and let
        # the frontend surface the "Transfer Request" button.
        holder_name = None
        if active_allocation.employee_id:
            holder = db.query(User).filter(User.id == active_allocation.employee_id).first()
            holder_name = holder.name if holder else None
        raise ConflictError(
            f"Asset '{asset.asset_tag}' is currently held by "
            f"{holder_name or ('department #' + str(active_allocation.department_id))}. "
            f"Use the Transfer Request flow instead."
        )

    if asset.status not in (AssetStatusEnum.AVAILABLE,):
        raise ConflictError(f"Asset is '{asset.status.value}' and cannot be allocated right now")

    allocation = AssetAllocation(
        asset_id=asset.id,
        employee_id=payload.employee_id,
        department_id=payload.department_id,
        expected_return_date=payload.expected_return_date,
        status=AllocationStatusEnum.ACTIVE,
        allocated_by=actor.id,
    )
    db.add(allocation)

    transition_status(asset, AssetStatusEnum.ALLOCATED)

    db.commit()
    db.refresh(allocation)

    if payload.employee_id:
        notification_service.create_notification(
            db,
            user_id=payload.employee_id,
            type_=NotificationTypeEnum.ASSET_ASSIGNED,
            message=f"Asset '{asset.name}' ({asset.asset_tag}) has been allocated to you.",
            related_entity_type="asset",
            related_entity_id=asset.id,
        )

    audit_log_service.log_action(
        db, user_id=actor.id, action="ASSET_ALLOCATED", entity_type="allocation", entity_id=allocation.id,
        details=asset.asset_tag,
    )
    return {"allocation": allocation, "asset": asset}


def return_asset(db: Session, payload: AllocationReturn, actor: User) -> AssetAllocation:
    allocation = db.query(AssetAllocation).filter(AssetAllocation.id == payload.allocation_id).first()
    if not allocation:
        raise NotFoundError("Allocation not found")
    if allocation.status != AllocationStatusEnum.ACTIVE:
        raise BadRequestError("This allocation is not currently active")

    asset = get_asset_or_404(db, allocation.asset_id)

    allocation.status = AllocationStatusEnum.RETURNED
    allocation.actual_return_date = datetime.now(timezone.utc)
    allocation.condition_checkin_notes = payload.condition_checkin_notes

    transition_status(asset, AssetStatusEnum.AVAILABLE)

    db.commit()
    db.refresh(allocation)

    audit_log_service.log_action(
        db, user_id=actor.id, action="ASSET_RETURNED", entity_type="allocation", entity_id=allocation.id
    )
    return allocation


def list_overdue_allocations(db: Session):
    today = datetime.now(timezone.utc).date()
    return (
        db.query(AssetAllocation)
        .filter(
            AssetAllocation.status == AllocationStatusEnum.ACTIVE,
            AssetAllocation.expected_return_date.isnot(None),
            AssetAllocation.expected_return_date < today,
        )
        .all()
    )


# ---------------------------------------------------------------------------
# Transfer workflow: Requested -> Approved (Asset Manager/Dept Head) -> Re-allocated
# ---------------------------------------------------------------------------

def request_transfer(db: Session, payload: TransferCreate, actor: User) -> TransferRequest:
    asset = get_asset_or_404(db, payload.asset_id)
    active_allocation = _get_active_allocation(db, asset.id)

    transfer = TransferRequest(
        asset_id=asset.id,
        from_employee_id=active_allocation.employee_id if active_allocation else None,
        to_employee_id=payload.to_employee_id,
        requested_by=actor.id,
        reason=payload.reason,
        status="requested",
    )
    db.add(transfer)

    if active_allocation:
        active_allocation.status = AllocationStatusEnum.TRANSFER_REQUESTED

    db.commit()
    db.refresh(transfer)

    notification_service.create_notification(
        db,
        user_id=payload.to_employee_id,
        type_=NotificationTypeEnum.TRANSFER_REQUESTED,
        message=f"A transfer request was raised for asset '{asset.name}' ({asset.asset_tag}).",
        related_entity_type="transfer_request",
        related_entity_id=transfer.id,
    )

    audit_log_service.log_action(
        db, user_id=actor.id, action="TRANSFER_REQUESTED", entity_type="transfer_request", entity_id=transfer.id
    )
    return transfer


def decide_transfer(db: Session, payload: TransferDecision, actor: User) -> TransferRequest:
    from app.models.enums import RoleEnum

    if actor.role not in (RoleEnum.ADMIN, RoleEnum.ASSET_MANAGER, RoleEnum.DEPARTMENT_HEAD):
        raise ForbiddenError("Only an Asset Manager or Department Head can approve transfers")

    transfer = db.query(TransferRequest).filter(TransferRequest.id == payload.transfer_id).first()
    if not transfer:
        raise NotFoundError("Transfer request not found")
    if transfer.status != "requested":
        raise BadRequestError("This transfer request has already been resolved")

    asset = get_asset_or_404(db, transfer.asset_id)
    old_active = _get_active_allocation(db, asset.id)

    transfer.approved_by = actor.id
    transfer.resolved_at = datetime.now(timezone.utc)

    if payload.approve:
        transfer.status = "approved"

        if old_active:
            old_active.status = AllocationStatusEnum.RETURNED
            old_active.actual_return_date = datetime.now(timezone.utc)

        new_allocation = AssetAllocation(
            asset_id=asset.id,
            employee_id=transfer.to_employee_id,
            status=AllocationStatusEnum.ACTIVE,
            allocated_by=actor.id,
        )
        db.add(new_allocation)
        transition_status(asset, AssetStatusEnum.ALLOCATED)

        notification_service.create_notification(
            db,
            user_id=transfer.to_employee_id,
            type_=NotificationTypeEnum.TRANSFER_APPROVED,
            message=f"Transfer approved: asset '{asset.name}' ({asset.asset_tag}) is now allocated to you.",
            related_entity_type="asset",
            related_entity_id=asset.id,
        )
    else:
        transfer.status = "rejected"
        transfer.reason = payload.reason or transfer.reason
        if old_active:
            old_active.status = AllocationStatusEnum.ACTIVE  # revert to active on rejection

    db.commit()
    db.refresh(transfer)

    audit_log_service.log_action(
        db, user_id=actor.id, action=f"TRANSFER_{transfer.status.upper()}",
        entity_type="transfer_request", entity_id=transfer.id,
    )
    return transfer
