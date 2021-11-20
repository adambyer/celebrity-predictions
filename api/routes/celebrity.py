from datetime import date, timedelta
from fastapi import Depends, HTTPException, status, APIRouter
from typing import List, Optional

from ..celebrity_utils import get_tweet_data
from ..crud.celebrity_crud import (
    get_celebrity_by_twitter_username,
    get_celebrities,
    get_celebrity_daily_metrics,
)
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
    limit: Optional[int] = 10,
    search: Optional[str] = None,
) -> list:
    try:
        if search:
            celebrities = get_celebrities(db, limit=limit, search=search)
        else:
            # Get the celebrities with the most activity.
            start_date = date.today() - timedelta(days=1)
            metrics = get_celebrity_daily_metrics(db, start_date=start_date, limit=10)
            celebrities = [
                metric.celebrity
                for metric in sorted(metrics, key=lambda m: m.total_count, reverse=True)
            ]
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
        tweet_data = get_tweet_data(db, db_celebrity)
        celebrity["tweets"] = tweet_data["tweets"]
        celebrity["metrics"] = tweet_data["metrics"]
        return celebrity

    return {}
