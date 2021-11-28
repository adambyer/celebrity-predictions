from fastapi import Depends, HTTPException, status, APIRouter
from typing import Dict, List

from ..db import Session
from ..model_types import LeaderType
from ..prediction_utils import get_leaders

from .dependencies import get_db


router = APIRouter(
    prefix="/prediction",
    tags=["prediction"],
    responses={404: {"description": "Not found"}},
)


@router.get("/leaders", response_model=Dict[str, List[LeaderType]])
async def get_leaders_route(
    db: Session = Depends(get_db),
) -> dict:
    try:
        leaders = get_leaders(db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown error.",
        ) from e

    return leaders
