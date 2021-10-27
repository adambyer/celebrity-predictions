from fastapi import Depends, HTTPException, APIRouter

from ..crud import get_user_by_username
from ..db import Session
from ..model_types import UserType, CurrentUserType

from .dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/me/", response_model=CurrentUserType)
async def get_current_user_route(
    current_user: CurrentUserType = Depends(get_current_user),
) -> CurrentUserType:
    return current_user


@router.get("/{username}", response_model=UserType)
def get_user_route(username: str, db: Session = Depends(get_db)) -> UserType:
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
