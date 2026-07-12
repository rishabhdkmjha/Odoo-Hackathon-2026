from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, require_admin
from app.database.database import get_db
from app.models.user import User
from app.schemas.user_schema import EmployeeCreate, EmployeeUpdate, UserOut
from app.services import user_service
from app.utils.response import success_response

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("")
def list_employees(
    department_id: Optional[int] = None,
    role: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Employee Directory listing - readable by any authenticated user."""
    employees = user_service.list_employees(db, department_id, role)
    return success_response(
        "Employees fetched successfully", [UserOut.model_validate(e).model_dump() for e in employees]
    )


@router.post("")
def create_employee(
    payload: EmployeeCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)
):
    """Admin creates an employee directly (bypassing self-signup)."""
    employee = user_service.create_employee(db, payload, current_user)
    return success_response("Employee created successfully", UserOut.model_validate(employee).model_dump())


@router.put("/{employee_id}")
def update_employee(
    employee_id: int,
    payload: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Admin-only. This is the ONLY endpoint that can promote an Employee to
    Department Head or Asset Manager.
    """
    employee = user_service.update_employee(db, employee_id, payload, current_user)
    return success_response("Employee updated successfully", UserOut.model_validate(employee).model_dump())


@router.delete("/{employee_id}")
def delete_employee(
    employee_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)
):
    user_service.delete_employee(db, employee_id, current_user)
    return success_response("Employee deleted successfully")
