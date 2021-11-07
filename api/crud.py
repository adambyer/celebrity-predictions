from datetime import date
from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload, raiseload
from typing import Optional, List

from .auth_utils import get_password_hash
from .db import engine
from .models import (
    Celebrity,
    CelebrityDailyMetrics,
    Prediction,
    PredictionResult,
    User,
)
from .model_types import (
    CelebrityDailyMetricsCreateType,
    CelebrityDailyMetricsType,
    CelebrityType,
    PredictionCreateType,
    PredictionType,
    PredictionResultCreateType,
    UserCreateType,
)


def get_user_by_username(
    db: Session,
    username: str,
) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def user_taken(
    db: Session,
    username: str,
    email_address: str,
) -> bool:
    return (
        db.query(User)
        .filter(
            or_(
                User.username == username,
                User.email_address == email_address,
            )
        )
        .first()
        is not None
    )


def create_user(
    db: Session,
    user: UserCreateType,
) -> User:
    password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email_address=user.email_address,
        password=password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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


def create_prediction_result(
    db: Session,
    prediction_result: PredictionResultCreateType,
) -> PredictionResult:
    db_prediction_result = PredictionResult(**prediction_result.dict())
    db.add(db_prediction_result)
    db.commit()
    db.refresh(db_prediction_result)
    return db_prediction_result


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


def get_user_predictions(
    db: Session,
    user_id: int,
) -> List[PredictionType]:
    return (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .join(Celebrity)
        .all()
    )


def create_celebrity_daily_metrics(
    db: Session,
    daily_metrics: CelebrityDailyMetricsCreateType,
) -> CelebrityDailyMetricsType:
    db_daily_metrics = CelebrityDailyMetrics(**daily_metrics.dict())
    db.add(db_daily_metrics)
    db.commit()
    db.refresh(db_daily_metrics)
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
