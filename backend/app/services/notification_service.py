"""
Central place to fire notifications. Called by other services whenever
a user-relevant event occurs (allocation, transfer, booking, maintenance,
overdue return, audit discrepancy).
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.enums import NotificationTypeEnum


def create_notification(
    db: Session,
    user_id: int,
    type_: NotificationTypeEnum,
    message: str,
    related_entity_type: Optional[str] = None,
    related_entity_id: Optional[int] = None,
) -> Notification:
    notification = Notification(
        user_id=user_id,
        type=type_,
        message=message,
        related_entity_type=related_entity_type,
        related_entity_id=related_entity_id,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


def get_notifications_for_user(db: Session, user_id: int, unread_only: bool = False):
    query = db.query(Notification).filter(Notification.user_id == user_id)
    if unread_only:
        query = query.filter(Notification.is_read.is_(False))
    return query.order_by(Notification.created_at.desc()).all()
