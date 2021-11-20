from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional, List

from ..auth_utils import get_password_hash
from ..models import (
    Celebrity,
    Prediction,
    User,
)
from ..model_types import (
    PredictionType,
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


def get_user_predictions(
    db: Session,
    user_id: int,
) -> List[PredictionType]:
    return (
        db.query(Prediction)
        .join(Celebrity)
        .filter(Prediction.user_id == user_id)
        .order_by(Prediction.created_at.desc())
        .all()
    )
