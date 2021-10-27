from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional

from ..crud import create_user, get_user_by_username
from ..db import Session
from ..models import User
from ..model_types import TokenType, UserCreateType, UserType
from ..auth_utils import create_access_token, verify_password

from .dependencies import get_db


router = APIRouter(
    prefix="",  # FastAPI docs doesn't work if this isn't at the root.
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


def _authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(db, username)

    if not user or not user.is_active:
        return None

    if not verify_password(password, user.password):
        return None

    return user


@router.post("/register", response_model=UserType)
async def register(
    user: UserCreateType,
    db: Session = Depends(get_db),
) -> dict:
    # TODO: validate password requirements.
    try:
        db_user = create_user(db, user)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email address is already registered.",
        ) from e

    return db_user


@router.post("/token", response_model=TokenType)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> dict:
    user = _authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
