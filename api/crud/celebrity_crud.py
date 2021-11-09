from datetime import date
from sqlalchemy.orm import Session, selectinload, raiseload
from typing import Optional, List

from ..db import engine
from ..models import (
    Celebrity,
    CelebrityDailyMetrics,
    Prediction,
)
from ..model_types import (
    CelebrityDailyMetricsCreateType,
    CelebrityDailyMetricsType,
    CelebrityType,
    PredictionCreateType,
)


def create_celebrity(
    db: Session,
    celebrity: CelebrityType,
) -> Celebrity:
    db_celebrity = Celebrity(**celebrity.dict())
    db.add(db_celebrity)
    db.commit()
    db.refresh(db_celebrity)
    return db_celebrity


def get_celebrity(
    db: Session,
    celebrity_id: int,
    include_predictions: bool = False
) -> Optional[Celebrity]:
    query = db.query(Celebrity).filter(Celebrity.id == celebrity_id)

    if include_predictions:
        query = query.options(selectinload("predictions"), raiseload("*"))

    # query = query.options(raiseload("*"))
    return query.first()


def get_celebrity_by_twitter_username(
    db: Session,
    twitter_username: str,
) -> Optional[Celebrity]:
    return (
        db.query(Celebrity)
        .filter(Celebrity.twitter_username == twitter_username)
        .first()
    )


def update_celebrity(
    db: Optional[Session],
    celebrity: Celebrity,
    **kwargs: str,
) -> None:
    # TODO: this is kinda awkward
    if db:
        for key, value in kwargs.items():
            setattr(celebrity, key, value)

        db.commit()
    else:
        with engine.begin() as connection:
            table = Celebrity.__table__
            connection.execute(
                table.update().where(table.c.id == celebrity.id).values(**kwargs)
            )


def get_celebrities(
    db: Session,
    offset: int = 0,
    limit: int = None,
) -> List[Celebrity]:
    query = (
        db.query(Celebrity)
        .filter(Celebrity.twitter_id.isnot(None))
        .options(raiseload("*"))
    )

    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(limit)

    return query.all()


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


def create_celebrity_daily_metrics(
    db: Session,
    daily_metrics: CelebrityDailyMetricsCreateType,
) -> CelebrityDailyMetricsType:
    print("*** create_celebrity_daily_metrics", daily_metrics)
    db_daily_metrics = CelebrityDailyMetrics(**daily_metrics.dict())
    print("*** create_celebrity_daily_metrics db_daily_metrics", db_daily_metrics)
    db.add(db_daily_metrics)
    print("*** create_celebrity_daily_metrics after add")
    db.commit()
    print("*** create_celebrity_daily_metrics after commit")
    db.refresh(db_daily_metrics)
    print("*** create_celebrity_daily_metrics after refresh")
    return db_daily_metrics


def get_celebrity_daily_metrics(
    db: Session,
    celebrity_id: int,
    metric_date: date,
) -> Optional[CelebrityDailyMetricsType]:
    return (
        db.query(CelebrityDailyMetrics)
        .filter(
            CelebrityDailyMetrics.celebrity_id == celebrity_id,
            CelebrityDailyMetrics.metric_date == metric_date,
        )
        .options(raiseload("*"))
        .first()
    )
