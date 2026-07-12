"""
Signup / login business logic.
Signup ALWAYS creates a plain Employee account - no role selection at signup.
Role elevation only happens via Admin (see user_service.update_employee).
"""
from sqlalchemy.orm import Session

from app.auth.security import hash_password, verify_password, create_access_token
from app.models.user import User
from app.models.enums import RoleEnum, UserStatusEnum
from app.schemas.auth_schema import SignupRequest, LoginRequest
from app.services import audit_log_service
from app.utils.exceptions import BadRequestError, ForbiddenError


def signup(db: Session, payload: SignupRequest) -> User:
    existing = db.query(User).filter(User.email == payload.email).first()
    if existing:
        raise BadRequestError("An account with this email already exists")

    user = User(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        role=RoleEnum.EMPLOYEE,  # hard-coded: no self-elevation possible
        status=UserStatusEnum.ACTIVE,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    audit_log_service.log_action(
        db, user_id=user.id, action="USER_SIGNUP", entity_type="user", entity_id=user.id
    )
    return user


def login(db: Session, payload: LoginRequest) -> tuple[User, str]:
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise BadRequestError("Invalid email or password")

    if user.status == UserStatusEnum.INACTIVE:
        raise ForbiddenError("This account has been deactivated. Contact your Admin.")

    token = create_access_token(data={"sub": str(user.id), "role": user.role.value})

    audit_log_service.log_action(
        db, user_id=user.id, action="USER_LOGIN", entity_type="user", entity_id=user.id
    )
    return user, token
