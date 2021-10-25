from fastapi import Depends, HTTPException, status, APIRouter
from typing import List

from api.celebrity_utils import get_tweets
from api.crud import get_celebrity_by_twitter_username, get_celebrities
from api.db import Session
from api.types import CelebrityType

from .dependencies import get_db


# These routes do not require authentication.
router = APIRouter(
    prefix="/celebrity",
    tags=["celebrity"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CelebrityType])
async def get_celebrities_route(
    db: Session = Depends(get_db),
) -> list:
    try:
        celebrities = get_celebrities(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown error.",
        ) from e

    return celebrities


@router.get("/{twitter_username}", response_model=CelebrityType)
async def get_celebrity_route(
    twitter_username: str,
    db: Session = Depends(get_db),
) -> dict:
    try:
        db_celebrity = get_celebrity_by_twitter_username(db, twitter_username)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid twitter username.",
        ) from e

    if db_celebrity:
        celebrity = db_celebrity.__dict__
        print("*** celebrity", celebrity)
        celebrity["tweets"] = get_tweets(db_celebrity)
        return celebrity

    return {}
