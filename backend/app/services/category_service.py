from sqlalchemy.orm import Session

from app.models.category import AssetCategory
from app.models.user import User
from app.schemas.category_schema import CategoryCreate
from app.services import audit_log_service
from app.utils.exceptions import BadRequestError


def list_categories(db: Session):
    return db.query(AssetCategory).order_by(AssetCategory.name).all()


def create_category(db: Session, payload: CategoryCreate, actor: User) -> AssetCategory:
    existing = db.query(AssetCategory).filter(AssetCategory.name == payload.name).first()
    if existing:
        raise BadRequestError("A category with this name already exists")

    category = AssetCategory(
        name=payload.name,
        description=payload.description,
        extra_fields=payload.extra_fields or {},
    )
    db.add(category)
    db.commit()
    db.refresh(category)

    audit_log_service.log_action(
        db, user_id=actor.id, action="CATEGORY_CREATED", entity_type="asset_category", entity_id=category.id
    )
    return category
