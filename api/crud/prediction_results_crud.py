from datetime import date
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from ..models import (
    PredictionResult,
    User,
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
    actual: int,
    points: int,
) -> PredictionResult:
    prediction_result.actual = actual
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


def get_scored_prediction_results(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> List[PredictionResult]:
    query = (
        db.query(PredictionResult)
        .options(
            joinedload(PredictionResult.user),
        )
        .where(PredictionResult.points.isnot(None))
    )

    if start_date:
        query = query.filter(PredictionResult.metric_date >= start_date)

    if end_date:
        query = query.filter(PredictionResult.metric_date <= end_date)

    return query.all()


def get_user_points_by_date(
    db: Session,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> list:
    query = (
        db.query(
            PredictionResult.user_id,
            User.username,
            PredictionResult.metric_date,
            func.sum(PredictionResult.points).label("total_points"),
        )
        .join(
            User,
        )
        .where(PredictionResult.points.isnot(None))
        .group_by(
            PredictionResult.user_id,
            User.username,
            PredictionResult.metric_date
        )
    )

    if start_date:
        query = query.filter(PredictionResult.metric_date >= start_date)

    if end_date:
        query = query.filter(PredictionResult.metric_date <= end_date)

    return [dict(r) for r in query.all()]
