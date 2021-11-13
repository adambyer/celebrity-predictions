from fastapi import Depends, HTTPException, status, APIRouter
from typing import List

from ..crud.prediction_crud import get_predictions
from ..db import Session
from ..model_types import PredictionType

from .dependencies import get_db


router = APIRouter(
    prefix="/prediction",
    tags=["prediction"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[PredictionType])
async def get_recent_predictions(
    db: Session = Depends(get_db),
) -> list:
    try:
        predictions = get_predictions(db, 10)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown error.",
        ) from e

    return predictions
