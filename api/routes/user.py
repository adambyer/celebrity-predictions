from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, APIRouter, status
from typing import List

from ..crud.prediction_crud import (
    create_prediction,
    delete_prediction,
    get_prediction,
    get_user_predictions,
    update_prediction,
)
from ..crud.prediction_results import (
    get_prediction_results_by_user_id,
)
from ..crud.user_crud import get_user_by_username
from ..db import Session
from ..models import User
from ..model_types import (
    CurrentUserType,
    PredictionBaseType,
    PredictionCreateType,
    PredictionType,
    PredictionUpdateType,
    PredictionResultType,
    UserType,
)

from .dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/me", response_model=CurrentUserType)
async def get_current_user_route(
    current_user: User = Depends(get_current_user),
) -> dict:
    return current_user


@router.get("/prediction", response_model=List[PredictionType])
def get_user_predictions_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    try:
        predictions = get_user_predictions(db, current_user.id)
    except Exception:
        raise HTTPException(status_code=400, detail="Unknown error.")

    return predictions


@router.post("/prediction", response_model=PredictionType)
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


@router.patch("/prediction/{prediction_id}", response_model=PredictionType)
def patch_user_predictions_route(
    prediction_id: int,
    prediction_: PredictionUpdateType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PredictionType:
    prediction = get_prediction(db, prediction_id)

    if not prediction:
        raise HTTPException(status_code=400, detail="Invalid id.")

    if prediction.user_id != current_user.id:
        raise HTTPException(status_code=401, detail="Access denied.")

    try:
        updated_prediction = update_prediction(db, prediction, **prediction_.dict())
    except Exception:
        raise HTTPException(status_code=400, detail="Unknown error.")

    return updated_prediction


@router.delete("/prediction/{prediction_id}")
async def delete_prediction_route(
    prediction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> bool:
    try:
        delete_prediction(db, prediction_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unknown error.",
        ) from e

    return True


@router.get("/prediction-results/locked", response_model=List[PredictionResultType])
def get_user_locked_prediction_results_route(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list:
    """Get yesterday's prediction results that are locked and waiting to be scored."""
    metric_date = datetime.utcnow().date() - timedelta(days=1)
    try:
        prediction_results = get_prediction_results_by_user_id(db, current_user.id, metric_date)
    except Exception:
        raise HTTPException(status_code=400, detail="Unknown error.")

    return prediction_results


# This must be last so that it doesn't handle the `prediction` endpoints.
@router.get("/{username}", response_model=UserType)
def get_user_route(
    username: str,
    db: Session = Depends(get_db),
) -> dict:
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
