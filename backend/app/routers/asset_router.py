from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_asset_manager
from app.database.database import get_db
from app.models.enums import AssetStatusEnum
from app.models.user import User
from app.schemas.asset_schema import AssetCreate, AssetUpdate, AssetOut
from app.services import asset_service
from app.utils.response import success_response

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.get("")
def list_assets(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    status: Optional[AssetStatusEnum] = None,
    department_id: Optional[int] = None,
    location: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search/filter by tag, serial number, QR code, category, status, department, or location (Screen 4)."""
    assets = asset_service.list_assets(db, search, category_id, status, department_id, location)
    return success_response(
        "Assets fetched successfully", [AssetOut.model_validate(a).model_dump() for a in assets]
    )


@router.get("/{asset_id}/history")
def get_asset_history(
    asset_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Per-asset allocation + maintenance history."""
    history = asset_service.get_asset_history(db, asset_id)
    return success_response("Asset history fetched successfully", history)


@router.post("")
def create_asset(
    payload: AssetCreate, db: Session = Depends(get_db), current_user: User = Depends(require_asset_manager)
):
    """Asset Manager/Admin registers a new asset. Auto-generates the asset tag."""
    asset = asset_service.create_asset(db, payload, current_user)
    return success_response("Asset registered successfully", AssetOut.model_validate(asset).model_dump())


@router.put("/{asset_id}")
def update_asset(
    asset_id: int,
    payload: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_asset_manager),
):
    asset = asset_service.update_asset(db, asset_id, payload, current_user)
    return success_response("Asset updated successfully", AssetOut.model_validate(asset).model_dump())


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_asset_manager)
):
    asset_service.delete_asset(db, asset_id, current_user)
    return success_response("Asset deleted successfully")
