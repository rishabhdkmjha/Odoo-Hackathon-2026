from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_admin
from app.database.database import get_db
from app.models.user import User
from app.schemas.category_schema import CategoryCreate, CategoryOut
from app.services import category_service
from app.utils.response import success_response

router = APIRouter(prefix="/categories", tags=["Asset Categories"])


@router.get("")
def list_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    categories = category_service.list_categories(db)
    return success_response(
        "Categories fetched successfully", [CategoryOut.model_validate(c).model_dump() for c in categories]
    )


@router.post("")
def create_category(
    payload: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)
):
    """Admin-only (Organization Setup, Screen 3 Tab B)."""
    category = category_service.create_category(db, payload, current_user)
    return success_response("Category created successfully", CategoryOut.model_validate(category).model_dump())
