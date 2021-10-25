from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Boolean,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .db import Base


class BaseMixin:
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())


class User(BaseMixin, Base):
    __tablename__ = "user"

    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    email_address = Column(String(120), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_staff = Column(Boolean, default=False, nullable=False)

    predictions = relationship("Prediction", backref="user")

    def __repr__(self) -> str:
        return f"{self.username} ({self.id})"


class Celebrity(BaseMixin, Base):
    __tablename__ = "celebrity"

    twitter_username = Column(String(100), unique=True, nullable=False)
    twitter_verified = Column(Boolean, default=False, nullable=False)

    # These are nullable because we will start with their username and then fetch the rest.
    twitter_id = Column(BigInteger(), unique=True)
    twitter_name = Column(String(100))
    twitter_profile_image_url = Column(String(1000))
    twitter_description = Column(String(1000))

    predictions = relationship("Prediction", backref="celebrity")

    def __repr__(self) -> str:
        return f"{self.twitter_username} ({self.id})"


class Prediction(BaseMixin, Base):
    __tablename__ = "prediction"

    user_id = Column(Integer, ForeignKey("user.id"))
    celebrity_id = Column(Integer, ForeignKey("celebrity.id"))

    is_enabled = Column(Boolean, default=True, nullable=False)
    is_auto_disabled = Column(Boolean, default=False, nullable=False)
    amount = Column(Integer, nullable=False)

    results = relationship("PredictionResult", backref="prediction")

    def __repr__(self) -> str:
        return f"user:{self.user_id} celebrity:{self.celebrity_id} amount:{self.amount} ({self.id})"


class PredictionResult(BaseMixin, Base):
    __tablename__ = "prediction_result"

    prediction_id = Column(Integer, ForeignKey("prediction.id"))

    # Amount can change on the prediction, so we need to maintain it from the day the prediction was run.
    amount = Column(Integer, nullable=False)

    points = Column(Integer, nullable=False)
