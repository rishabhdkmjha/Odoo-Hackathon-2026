from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.services import dashboard_service
from app.utils.response import success_response

router = APIRouter(tags=["Dashboard"])


@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Real-time operational snapshot: KPI cards + overdue highlights (Screen 2)."""
    data = dashboard_service.get_dashboard_data(db, current_user)
    return success_response("Dashboard data fetched successfully", data)
