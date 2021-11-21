from datetime import date
from sqlalchemy import update
from sqlalchemy.orm import Session, selectinload, raiseload
from sqlalchemy.sql.expression import or_
from typing import Optional, List

from ..db import engine
from ..models import (
    Celebrity,
    CelebrityDailyMetrics,
)
from ..model_types import (
    CelebrityDailyMetricsCreateType,
    CelebrityDailyMetricsType,
    CelebrityCreateType,
)


def create_celebrity(
    db: Session,
    celebrity: CelebrityCreateType,
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
    search: str = None,
) -> List[Celebrity]:
    query = (
        db.query(Celebrity)
        .filter(Celebrity.twitter_id.isnot(None))
        .options(raiseload("*"))
    )

    if search:
        query = query.filter(
            or_(
                Celebrity.twitter_username.ilike(f"%{search}%"),
                Celebrity.twitter_name.ilike(f"%{search}%"),
            )
        )

    if offset:
        query = query.offset(offset)

    if limit:
        query = query.limit(limit)

    return query.all()


def create_celebrity_daily_metrics(
    db: Session,
    metrics: CelebrityDailyMetricsCreateType,
) -> CelebrityDailyMetricsType:
    db_daily_metrics = CelebrityDailyMetrics(**metrics.dict())
    db.add(db_daily_metrics)
    db.commit()
    db.refresh(db_daily_metrics)
    return db_daily_metrics


def get_celebrity_daily_metrics(
    db: Session,
    celebrity_id: int,
    metric_date: date,
) -> Optional[CelebrityDailyMetrics]:
    return (
        db.query(CelebrityDailyMetrics)
        .filter(
            CelebrityDailyMetrics.celebrity_id == celebrity_id,
            CelebrityDailyMetrics.metric_date == metric_date,
        ).first()
    )


def update_celebrity_daily_metrics(
    db: Session,
    id_: int,
    updates: CelebrityDailyMetricsCreateType,
) -> None:
    db.execute(
        update(CelebrityDailyMetrics)
        .where(CelebrityDailyMetrics.id == id_)
        .values(**updates.dict())
    )


def get_celebrity_daily_metrics_list(
    db: Session,
    celebrity_ids: list = None,
    start_date: date = None,
    end_date: date = None,
    limit: int = None,
) -> list:
    query = (
        db.query(CelebrityDailyMetrics)
        .join(Celebrity)
    )

    if celebrity_ids:
        query = query.filter(
            CelebrityDailyMetrics.celebrity_id.in_(celebrity_ids),
        )

    if start_date:
        query = query.filter(
            CelebrityDailyMetrics.metric_date >= start_date,
        )

    if end_date:
        query = query.filter(
            CelebrityDailyMetrics.metric_date <= end_date,
        )

    query = (
        query
        .order_by(CelebrityDailyMetrics.created_at.desc())

        # TODO: How to do this for all relationships other than those defined above?
        # .options(raiseload("*"))
    )

    if limit:
        query = query.limit(limit)

    return query.all()
