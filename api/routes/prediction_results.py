from fastapi import Depends, HTTPException, status, APIRouter
from typing import List

from ..db import Session
from ..model_types import LeaderType
from ..prediction_results_utils import (
    get_leaders_all_time,
    get_leaders_daily,
)

from .dependencies import get_db


router = APIRouter(
    prefix="/prediction-results",
    tags=["prediction-results"],
    responses={404: {"description": "Not found"}},
)


@router.get("/leaders/all-time", response_model=List[LeaderType])
async def get_leaders_all_time_route(
    db: Session = Depends(get_db),
) -> list:
    try:
        leaders = get_leaders_all_time(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown error.",
        ) from e

    return leaders


@router.get("/leaders/daily", response_model=List[LeaderType])
async def get_leaders_daily_route(
    db: Session = Depends(get_db),
) -> list:
    try:
        leaders = get_leaders_daily(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown error.",
        ) from e

    return leaders
