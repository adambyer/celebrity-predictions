from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from api.db import Session
from api.types import TokenType
from .auth_utils import authenticate_user, create_access_token
from .dependencies import get_db

router = APIRouter(
    prefix="",  # FastAPI docs doesn't work if this isn't at the root.
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=TokenType)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> dict:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )
    return {"access_token": access_token, "token_type": "bearer"}