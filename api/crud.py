from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional

from .auth_utils import get_password_hash
from .db import engine
from .models import (
    Celebrity,
    User,
)
from .types import (
    CelebrityBaseType,
    UserCreateType,
)


def get_user_by_username(
    db: Session,
    username: str,
):
    return db.query(User).filter(User.username == username).first()


def user_taken(
    db: Session,
    username: str,
    email_address: str,
):
    return db.query(User).filter(
        or_(
            User.username == username,
            User.email_address == email_address,
        )
    ).first() is not None


def create_user(
    db: Session,
    user: UserCreateType,
):
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
    celebrity: CelebrityBaseType,
):
    db_celebrity = Celebrity(**celebrity.dict())
    db.add(db_celebrity)
    db.commit()
    db.refresh(db_celebrity)
    return db_celebrity


def get_celebrity(
    db: Session,
    celebrity_id: int,
):
    return db.query(Celebrity).filter(Celebrity.id == celebrity_id).first()


def update_celebrity(
    db: Optional[Session],
    celebrity: Celebrity,
    **kwargs,
):
    if db:
        for key, value in kwargs.items():
            setattr(celebrity, key, value)

        db.commit()
    else:
        with engine.begin() as connection:
            table = Celebrity.__table__
            connection.execute(
                table.update().
                where(table.c.id == celebrity.id).
                values(**kwargs)
            )


def get_celebrities(skip: int = 0, limit: int = 100, db: Session = None):
    return db.query(Celebrity).offset(skip).limit(limit).all()
