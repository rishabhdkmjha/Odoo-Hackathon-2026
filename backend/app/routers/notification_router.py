from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.notification_schema import NotificationOut
from app.services import notification_service
from app.utils.response import success_response

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("")
def get_notifications(
    unread_only: bool = False, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    """Per-user notification feed (Screen 10)."""
    notifications = notification_service.get_notifications_for_user(db, current_user.id, unread_only)
    return success_response(
        "Notifications fetched successfully",
        [NotificationOut.model_validate(n).model_dump() for n in notifications],
    )
