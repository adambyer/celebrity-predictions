from fastapi import Depends, HTTPException, status, APIRouter
from typing import List

from ..celebrity_utils import get_tweet_data
from ..crud.celebrity_crud import get_celebrity_by_twitter_username, get_celebrities
from ..db import Session
from ..model_types import CelebrityType

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

        # TODO: paging for tweets.
        tweet_data = get_tweet_data(db_celebrity)
        celebrity["tweets"] = tweet_data["tweets"]
        celebrity["metrics"] = tweet_data["metrics"]
        return celebrity

    return {}
