from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.enums import NotificationTypeEnum


class NotificationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    type: NotificationTypeEnum
    message: str
    related_entity_type: Optional[str] = None
    related_entity_id: Optional[int] = None
    is_read: bool
    created_at: datetime
