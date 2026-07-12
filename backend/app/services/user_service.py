"""
Employee Directory business logic (Admin-only, Screen 3 Tab C).
This is the ONLY place a user's role can change - promotions to
Department Head / Asset Manager happen exclusively through update_employee.
"""
from typing import Optional

from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.models.user import User
from app.schemas.user_schema import EmployeeCreate, EmployeeUpdate
from app.services import audit_log_service
from app.utils.exceptions import NotFoundError, BadRequestError


def list_employees(db: Session, department_id: Optional[int] = None, role: Optional[str] = None):
    query = db.query(User)
    if department_id is not None:
        query = query.filter(User.department_id == department_id)
    if role is not None:
        query = query.filter(User.role == role)
    return query.order_by(User.name).all()


def create_employee(db: Session, payload: EmployeeCreate, actor: User) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise BadRequestError("An account with this email already exists")

    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        department_id=payload.department_id,
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    audit_log_service.log_action(
        db, user_id=actor.id, action="EMPLOYEE_CREATED", entity_type="user", entity_id=user.id,
        details=f"role={user.role.value}",
    )
    return user


def update_employee(db: Session, employee_id: int, payload: EmployeeUpdate, actor: User) -> User:
    user = db.query(User).filter(User.id == employee_id).first()
    if not user:
        raise NotFoundError("Employee not found")

    changes = []
    if payload.name is not None:
        user.name = payload.name
    if payload.department_id is not None:
        user.department_id = payload.department_id
    if payload.role is not None and payload.role != user.role:
        changes.append(f"role {user.role.value}->{payload.role.value}")
        user.role = payload.role
    if payload.status is not None:
        user.status = payload.status

    db.commit()
    db.refresh(user)

    audit_log_service.log_action(
        db, user_id=actor.id, action="EMPLOYEE_UPDATED", entity_type="user", entity_id=user.id,
        details="; ".join(changes) if changes else None,
    )
    return user


def delete_employee(db: Session, employee_id: int, actor: User) -> None:
    user = db.query(User).filter(User.id == employee_id).first()
    if not user:
        raise NotFoundError("Employee not found")

    if user.id == actor.id:
        raise BadRequestError("You cannot delete your own account")

    db.delete(user)
    db.commit()

    audit_log_service.log_action(
        db, user_id=actor.id, action="EMPLOYEE_DELETED", entity_type="user", entity_id=employee_id
    )
