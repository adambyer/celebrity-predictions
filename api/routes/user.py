from datetime import datetime
from fastapi import Depends, HTTPException, APIRouter, status
from typing import List

from ..crud.celebrity_crud import (
    get_celebrity_daily_metrics_list,
)
from ..crud.prediction_crud import (
    create_prediction,
    delete_prediction,
    get_prediction,
    update_prediction,
)
from ..crud.prediction_results_crud import (
    get_prediction_results_by_user_id,
)
from ..crud.user_crud import (
    get_user_by_username,
    get_user_predictions,
    update_user,
)
from ..db import Session
from ..models import User
from ..model_types import (
    CurrentUserType,
    PredictionBaseType,
    PredictionCreateType,
    PredictionType,
    PredictionUpdateType,
    PredictionResultType,
    UserBaseType,
    UserUpdateType,
)

from .dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    # dependencies=[Depends(get_current_user)],
    responses={404: {"description": "Not found"}},
)


@router.get("/account", response_model=CurrentUserType)
async def get_current_user_route(
    current_user: User = Depends(get_current_user),
) -> dict:
    return current_user


@router.post("/account")
async def post_current_user_route(
    user: UserUpdateType,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    update_user(db, current_user.id, user)


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
    """Get today's prediction results that are locked and waiting to be scored."""
    metric_date = datetime.utcnow().date()
    try:
        prediction_results = get_prediction_results_by_user_id(db, current_user.id, metric_date)
        celebrity_ids = [pr.celebrity_id for pr in prediction_results]
        metrics = get_celebrity_daily_metrics_list(db, celebrity_ids, metric_date, metric_date)
        results = []

        for pr in prediction_results:
            result = pr.__dict__
            current = [getattr(m, f"{pr.metric}_count") for m in metrics if m.celebrity_id == pr.celebrity_id]

            results.append({
                **result,
                "current": current[0] if len(current) > 0 else None,
            })
    except Exception:
        raise HTTPException(status_code=400, detail="Unknown error.")

    return results


# This must be last so that it doesn't handle the `prediction` endpoints.
@router.get("/{username}", response_model=UserBaseType)
def get_user_route(
    username: str,
    db: Session = Depends(get_db),
) -> dict:
    user = get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user
