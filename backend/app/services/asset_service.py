from typing import Optional

from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.category import AssetCategory
from app.models.user import User
from app.models.enums import AssetStatusEnum
from app.schemas.asset_schema import AssetCreate, AssetUpdate
from app.services import audit_log_service
from app.utils.asset_tag import generate_asset_tag
from app.utils.exceptions import NotFoundError, BadRequestError, ConflictError


# Allowed lifecycle transitions. Keys = current status, values = statuses it can move to.
ALLOWED_TRANSITIONS = {
    AssetStatusEnum.AVAILABLE: {
        AssetStatusEnum.ALLOCATED,
        AssetStatusEnum.RESERVED,
        AssetStatusEnum.MAINTENANCE,
        AssetStatusEnum.LOST,
        AssetStatusEnum.DISPOSED,
    },
    AssetStatusEnum.ALLOCATED: {AssetStatusEnum.AVAILABLE, AssetStatusEnum.MAINTENANCE, AssetStatusEnum.LOST},
    AssetStatusEnum.RESERVED: {AssetStatusEnum.AVAILABLE, AssetStatusEnum.MAINTENANCE},
    AssetStatusEnum.MAINTENANCE: {AssetStatusEnum.AVAILABLE, AssetStatusEnum.LOST, AssetStatusEnum.DISPOSED},
    AssetStatusEnum.LOST: {AssetStatusEnum.AVAILABLE, AssetStatusEnum.DISPOSED},
    AssetStatusEnum.DISPOSED: set(),  # terminal state
}


def transition_status(asset: Asset, new_status: AssetStatusEnum) -> None:
    """Validates and applies a lifecycle transition. Raises ConflictError if illegal."""
    if asset.status == new_status:
        return
    allowed = ALLOWED_TRANSITIONS.get(asset.status, set())
    if new_status not in allowed:
        raise ConflictError(
            f"Cannot transition asset from '{asset.status.value}' to '{new_status.value}'"
        )
    asset.status = new_status


def list_assets(
    db: Session,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    status: Optional[AssetStatusEnum] = None,
    department_id: Optional[int] = None,
    location: Optional[str] = None,
):
    query = db.query(Asset)

    if search:
        like = f"%{search}%"
        query = query.filter(
            (Asset.asset_tag.ilike(like))
            | (Asset.serial_number.ilike(like))
            | (Asset.qr_code.ilike(like))
            | (Asset.name.ilike(like))
        )
    if category_id is not None:
        query = query.filter(Asset.category_id == category_id)
    if status is not None:
        query = query.filter(Asset.status == status)
    if department_id is not None:
        query = query.filter(Asset.department_id == department_id)
    if location:
        query = query.filter(Asset.location.ilike(f"%{location}%"))

    return query.order_by(Asset.created_at.desc()).all()


def get_asset_or_404(db: Session, asset_id: int) -> Asset:
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise NotFoundError("Asset not found")
    return asset


def create_asset(db: Session, payload: AssetCreate, actor: User) -> Asset:
    category = db.query(AssetCategory).filter(AssetCategory.id == payload.category_id).first()
    if not category:
        raise NotFoundError("Asset category not found")

    asset = Asset(
        name=payload.name,
        asset_tag=generate_asset_tag(db),
        category_id=payload.category_id,
        department_id=payload.department_id,
        serial_number=payload.serial_number,
        acquisition_date=payload.acquisition_date,
        acquisition_cost=payload.acquisition_cost,
        condition=payload.condition,
        location=payload.location,
        is_bookable=payload.is_bookable,
        photo_url=payload.photo_url,
        document_url=payload.document_url,
        status=AssetStatusEnum.AVAILABLE,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)

    audit_log_service.log_action(
        db, user_id=actor.id, action="ASSET_REGISTERED", entity_type="asset", entity_id=asset.id,
        details=asset.asset_tag,
    )
    return asset


def update_asset(db: Session, asset_id: int, payload: AssetUpdate, actor: User) -> Asset:
    asset = get_asset_or_404(db, asset_id)
    data = payload.model_dump(exclude_unset=True)

    new_status = data.pop("status", None)
    for field, value in data.items():
        setattr(asset, field, value)

    if new_status is not None:
        transition_status(asset, new_status)

    db.commit()
    db.refresh(asset)

    audit_log_service.log_action(
        db, user_id=actor.id, action="ASSET_UPDATED", entity_type="asset", entity_id=asset.id
    )
    return asset


def delete_asset(db: Session, asset_id: int, actor: User) -> None:
    asset = get_asset_or_404(db, asset_id)
    db.delete(asset)
    db.commit()

    audit_log_service.log_action(
        db, user_id=actor.id, action="ASSET_DELETED", entity_type="asset", entity_id=asset_id
    )


def get_asset_history(db: Session, asset_id: int) -> dict:
    """Per-asset allocation + maintenance history, as required by Screen 4."""
    asset = get_asset_or_404(db, asset_id)
    return {
        "allocation_history": [
            {
                "id": a.id,
                "employee_id": a.employee_id,
                "department_id": a.department_id,
                "allocated_date": a.allocated_date,
                "expected_return_date": a.expected_return_date,
                "actual_return_date": a.actual_return_date,
                "status": a.status,
            }
            for a in asset.allocations
        ],
        "maintenance_history": [
            {
                "id": m.id,
                "issue_description": m.issue_description,
                "status": m.status,
                "priority": m.priority,
                "created_at": m.created_at,
                "resolved_at": m.resolved_at,
            }
            for m in asset.maintenance_requests
        ],
    }
