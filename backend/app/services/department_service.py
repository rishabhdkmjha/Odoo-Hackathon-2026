from typing import Optional

from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.user import User
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate
from app.services import audit_log_service
from app.utils.exceptions import NotFoundError, BadRequestError


def list_departments(db: Session):
    return db.query(Department).order_by(Department.name).all()


def create_department(db: Session, payload: DepartmentCreate, actor: User) -> Department:
    existing = db.query(Department).filter(Department.name == payload.name).first()
    if existing:
        raise BadRequestError("A department with this name already exists")

    if payload.parent_department_id:
        parent = db.query(Department).filter(Department.id == payload.parent_department_id).first()
        if not parent:
            raise NotFoundError("Parent department not found")

    department = Department(
        name=payload.name,
        head_id=payload.head_id,
        parent_department_id=payload.parent_department_id,
        status=payload.status,
    )
    db.add(department)
    db.commit()
    db.refresh(department)

    audit_log_service.log_action(
        db, user_id=actor.id, action="DEPARTMENT_CREATED", entity_type="department", entity_id=department.id
    )
    return department


def update_department(db: Session, department_id: int, payload: DepartmentUpdate, actor: User) -> Department:
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise NotFoundError("Department not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(department, field, value)

    db.commit()
    db.refresh(department)

    audit_log_service.log_action(
        db, user_id=actor.id, action="DEPARTMENT_UPDATED", entity_type="department", entity_id=department.id
    )
    return department
