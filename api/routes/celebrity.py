from datetime import datetime
from fastapi import Depends, HTTPException, status, APIRouter
import logging
from typing import List, Optional

from ..celebrity_utils import get_tweet_data
from ..crud.celebrity_crud import (
    get_celebrity_by_twitter_username,
    get_celebrities,
    get_celebrity_daily_metrics_list,
)
from ..db import Session
from ..model_types import (
    CelebrityType,
    CelebrityDailyMetricsType,
)

from .dependencies import get_db

logger = logging.getLogger(__name__)

# These routes do not require authentication.
router = APIRouter(
    prefix="/celebrity",
    tags=["celebrity"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CelebrityType])
async def get_celebrities_route(
    db: Session = Depends(get_db),
    limit: int = 10,
    search: Optional[str] = None,
) -> list:
    metric_date = datetime.utcnow().date()
    try:
        if search:
            db_celebrities = get_celebrities(db, limit=limit, search=search)
            metrics_lookup = {
                m.celebrity.id: CelebrityDailyMetricsType(**m.__dict__) for m in
                get_celebrity_daily_metrics_list(db, celebrity_ids=[c.id for c in db_celebrities], start_date=metric_date, end_date=metric_date)
            }
            celebrities = [
                {
                    **{k: v for k, v in c.__dict__.items()},
                    "metrics": [metrics_lookup[c.id]] if c.id in metrics_lookup else [],
                }
                for c in db_celebrities
            ]
        else:
            # Get the celebrities with the most activity today.
            metrics = get_celebrity_daily_metrics_list(db, start_date=datetime.utcnow().date())
            celebrities = [
                {
                    **{k: v for k, v in metric.celebrity.__dict__.items()},
                    "metrics": [CelebrityDailyMetricsType(**metric.__dict__)],
                }
                for metric in sorted(metrics, key=lambda m: m.total_count, reverse=True)
                if metric.total_count > 0
            ][:limit]
    except Exception as e:
        logger.exception("")
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
        logger.exception("")
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
