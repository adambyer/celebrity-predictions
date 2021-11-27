from datetime import date
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from ..models import (
    PredictionResult,
)
from ..model_types import (
    PredictionResultCreateType,
)


def create_prediction_result(
    db: Session,
    prediction_result: PredictionResultCreateType,
) -> PredictionResult:
    db_prediction_result = PredictionResult(**prediction_result.dict())
    db.add(db_prediction_result)
    db.commit()
    db.refresh(db_prediction_result)
    return db_prediction_result


def update_prediction_result(
    db: Session,
    prediction_result: PredictionResult,
    points: int,
) -> PredictionResult:
    prediction_result.points = points
    db.commit()
    db.refresh(prediction_result)
    return prediction_result


def get_prediction_results_for_scoring(
    db: Session,
    celebrity_id: int,
    metric_date: date,
) -> List[PredictionResult]:
    return (
        db.query(PredictionResult)
        .filter(
            PredictionResult.celebrity_id == celebrity_id,
            PredictionResult.metric_date == metric_date,
        )
        .all()
    )


def get_prediction_results_by_user_id(
    db: Session,
    user_id: int,
    metric_date: Optional[date] = None,
) -> List[PredictionResult]:
    query = (
        db.query(PredictionResult)
        .filter(
            PredictionResult.user_id == user_id,
        )
        .options(
            joinedload(PredictionResult.celebrity)
        )
    )

    if metric_date:
        query = query.filter(PredictionResult.metric_date == metric_date)

    return query.all()
