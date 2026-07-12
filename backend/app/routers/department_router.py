from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_admin
from app.database.database import get_db
from app.models.user import User
from app.schemas.department_schema import DepartmentCreate, DepartmentOut
from app.services import department_service
from app.utils.response import success_response

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("")
def list_departments(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    departments = department_service.list_departments(db)
    return success_response(
        "Departments fetched successfully", [DepartmentOut.model_validate(d).model_dump() for d in departments]
    )


@router.post("")
def create_department(
    payload: DepartmentCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)
):
    """Admin-only (Organization Setup, Screen 3 Tab A)."""
    department = department_service.create_department(db, payload, current_user)
    return success_response(
        "Department created successfully", DepartmentOut.model_validate(department).model_dump()
    )
