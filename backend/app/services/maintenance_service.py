"""
Maintenance Management business logic (Screen 7).

Workflow: Pending -> Approved/Rejected (Asset Manager) -> Technician Assigned
-> In Progress -> Resolved.
Asset auto-flips to MAINTENANCE on approval, back to AVAILABLE on resolution.
"""
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.maintenance import MaintenanceRequest
from app.models.user import User
from app.models.enums import MaintenanceStatusEnum, AssetStatusEnum, NotificationTypeEnum, RoleEnum
from app.schemas.maintenance_schema import MaintenanceCreate, MaintenanceUpdate
from app.services import audit_log_service, notification_service
from app.services.asset_service import get_asset_or_404, transition_status
from app.utils.exceptions import NotFoundError, BadRequestError, ForbiddenError, ConflictError


# Legal forward-transitions of a maintenance request
NEXT_ALLOWED = {
    MaintenanceStatusEnum.PENDING: {MaintenanceStatusEnum.APPROVED, MaintenanceStatusEnum.REJECTED},
    MaintenanceStatusEnum.APPROVED: {MaintenanceStatusEnum.TECHNICIAN_ASSIGNED},
    MaintenanceStatusEnum.TECHNICIAN_ASSIGNED: {MaintenanceStatusEnum.IN_PROGRESS},
    MaintenanceStatusEnum.IN_PROGRESS: {MaintenanceStatusEnum.RESOLVED},
    MaintenanceStatusEnum.REJECTED: set(),
    MaintenanceStatusEnum.RESOLVED: set(),
}


def list_maintenance_requests(db: Session, asset_id: Optional[int] = None, status: Optional[str] = None):
    query = db.query(MaintenanceRequest)
    if asset_id is not None:
        query = query.filter(MaintenanceRequest.asset_id == asset_id)
    if status is not None:
        query = query.filter(MaintenanceRequest.status == status)
    return query.order_by(MaintenanceRequest.created_at.desc()).all()


def create_maintenance_request(db: Session, payload: MaintenanceCreate, actor: User) -> MaintenanceRequest:
    asset = get_asset_or_404(db, payload.asset_id)

    request = MaintenanceRequest(
        asset_id=asset.id,
        raised_by=actor.id,
        issue_description=payload.issue_description,
        priority=payload.priority,
        photo_url=payload.photo_url,
        status=MaintenanceStatusEnum.PENDING,
    )
    db.add(request)
    db.commit()
    db.refresh(request)

    audit_log_service.log_action(
        db, user_id=actor.id, action="MAINTENANCE_REQUESTED", entity_type="maintenance_request",
        entity_id=request.id,
    )
    return request


def update_maintenance_request(
    db: Session, request_id: int, payload: MaintenanceUpdate, actor: User
) -> MaintenanceRequest:
    request = db.query(MaintenanceRequest).filter(MaintenanceRequest.id == request_id).first()
    if not request:
        raise NotFoundError("Maintenance request not found")

    asset = get_asset_or_404(db, request.asset_id)

    if payload.status is not None and payload.status != request.status:
        allowed_next = NEXT_ALLOWED.get(request.status, set())
        if payload.status not in allowed_next:
            raise ConflictError(
                f"Cannot move maintenance request from '{request.status.value}' to '{payload.status.value}'"
            )

        if payload.status in (MaintenanceStatusEnum.APPROVED, MaintenanceStatusEnum.REJECTED):
            if actor.role not in (RoleEnum.ADMIN, RoleEnum.ASSET_MANAGER):
                raise ForbiddenError("Only an Asset Manager can approve or reject maintenance requests")
            request.approved_by = actor.id

        if payload.status == MaintenanceStatusEnum.APPROVED:
            transition_status(asset, AssetStatusEnum.MAINTENANCE)
            notification_service.create_notification(
                db, user_id=request.raised_by, type_=NotificationTypeEnum.MAINTENANCE_APPROVED,
                message=f"Maintenance request for '{asset.name}' was approved.",
                related_entity_type="maintenance_request", related_entity_id=request.id,
            )
        elif payload.status == MaintenanceStatusEnum.REJECTED:
            notification_service.create_notification(
                db, user_id=request.raised_by, type_=NotificationTypeEnum.MAINTENANCE_REJECTED,
                message=f"Maintenance request for '{asset.name}' was rejected.",
                related_entity_type="maintenance_request", related_entity_id=request.id,
            )
        elif payload.status == MaintenanceStatusEnum.RESOLVED:
            transition_status(asset, AssetStatusEnum.AVAILABLE)
            request.resolved_at = datetime.now(timezone.utc)

        request.status = payload.status

    if payload.technician_name is not None:
        request.technician_name = payload.technician_name
    if payload.resolution_notes is not None:
        request.resolution_notes = payload.resolution_notes

    db.commit()
    db.refresh(request)

    audit_log_service.log_action(
        db, user_id=actor.id, action="MAINTENANCE_UPDATED", entity_type="maintenance_request",
        entity_id=request.id, details=request.status.value,
    )
    return request
