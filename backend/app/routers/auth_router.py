from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schemas.auth_schema import SignupRequest, LoginRequest
from app.schemas.user_schema import UserOut
from app.services import auth_service
from app.utils.response import success_response

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    """Creates a plain Employee account. No role selection at signup."""
    user = auth_service.signup(db, payload)
    return success_response("Account created successfully", UserOut.model_validate(user).model_dump())


@router.post("/login")
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user, token = auth_service.login(db, payload)
    return success_response(
        "Login successful",
        {
            "access_token": token,
            "token_type": "bearer",
            "user": UserOut.model_validate(user).model_dump(),
        },
    )
