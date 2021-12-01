from sqlalchemy.orm import Session, raiseload
from typing import Optional, List

from ..models import (
    Prediction,
)
from ..model_types import (
    PredictionCreateType,
)


def create_prediction(
    db: Session,
    prediction: PredictionCreateType,
) -> Prediction:
    db_prediction = Prediction(**prediction.dict())
    db.add(db_prediction)
    db.commit()
    db.refresh(db_prediction)
    return db_prediction


def get_prediction(
    db: Session,
    prediction_id: int,
) -> Prediction:
    return (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )


def update_prediction(
    db: Session,
    prediction: Prediction,
    metric: Optional[str],
    amount: Optional[int],
    is_enabled: Optional[bool],
    is_auto_disabled: Optional[bool],
) -> Prediction:
    if metric:
        prediction.metric = metric

    if amount:
        prediction.amount = amount

    if is_enabled is not None:
        prediction.is_enabled = is_enabled

    if is_auto_disabled is not None:
        prediction.is_auto_disabled = is_auto_disabled

    db.commit()
    db.refresh(prediction)
    return prediction


def delete_prediction(
    db: Session,
    prediction_id: int,
) -> None:
    prediction = (
        db.query(Prediction)
        .filter(Prediction.id == prediction_id)
        .first()
    )
    db.delete(prediction)
    db.commit()


def get_predictions(
    db: Session,
    limit: Optional[int] = None,
) -> List[Prediction]:
    query = (
        db.query(Prediction)
        .filter(Prediction.is_enabled.is_(True))
        .order_by(Prediction.created_at.desc())
        .options(raiseload("*"))
    )

    if limit:
        query = query.limit(limit)

    return query.all()
