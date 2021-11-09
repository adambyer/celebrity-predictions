from fastapi import Depends, HTTPException, status, APIRouter
from typing import List

from ..crud.prediction_crud import create_prediction, get_predictions
from ..db import Session
from ..models import User
from ..model_types import PredictionType, PredictionBaseType, PredictionCreateType

from .dependencies import get_db, get_current_user


router = APIRouter(
    prefix="/prediction",
    tags=["prediction"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=PredictionType)
async def create_prediction_route(
    prediction: PredictionBaseType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    prediction = PredictionCreateType(**prediction.dict(), user_id=current_user.id)
    try:
        db_prediction = create_prediction(db, prediction)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown error.",
        ) from e

    return db_prediction


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
