from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.services import report_service
from app.utils.response import success_response

router = APIRouter(tags=["Reports"])


@router.get("/reports")
def get_reports(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Actionable operational insight: utilization, maintenance frequency, heatmaps (Screen 9)."""
    data = report_service.get_reports(db)
    return success_response("Reports fetched successfully", data)
