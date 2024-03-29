from datetime import datetime
from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Integer,
    String,
    Boolean,
    BigInteger,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.ext.hybrid import hybrid_property
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

    predictions = relationship("Prediction", backref="user", cascade="all, delete-orphan")
    prediction_results = relationship("PredictionResult", backref="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.username} ({self.id})"


class Celebrity(BaseMixin, Base):
    __tablename__ = "celebrity"

    twitter_username = Column(String(100), unique=True, nullable=False)
    twitter_verified = Column(Boolean, default=False, nullable=False)

    # These are nullable because we will start with their username and then fetch the rest.
    twitter_id = Column(BigInteger(), unique=True)
    twitter_name = Column(String(100))
    twitter_description = Column(String(1000))

    # We take this from the Twitter API as is.
    # It comes with a "_normal" suffix but that can be replaced to get other sizes.
    # https://developer.twitter.com/en/docs/twitter-api/v1/accounts-and-users/user-profile-images-and-banners
    twitter_profile_image_url = Column(String(1000))

    predictions = relationship("Prediction", backref="celebrity", cascade="all, delete-orphan")
    prediction_results = relationship("PredictionResult", backref="celebrity", cascade="all, delete-orphan")
    daily_metrics = relationship("CelebrityDailyMetrics", backref="celebrity", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"{self.twitter_username} ({self.id})"


class CelebrityDailyMetrics(BaseMixin, Base):
    __tablename__ = "celebrity_daily_metrics"
    __table_args__ = (
        UniqueConstraint('celebrity_id', 'metric_date'),
    )

    celebrity_id = Column(Integer, ForeignKey("celebrity.id", ondelete="CASCADE"), nullable=False)
    metric_date = Column(Date, nullable=False)
    like_count = Column(Integer, nullable=False)
    quote_count = Column(Integer, nullable=False)
    reply_count = Column(Integer, nullable=False)
    retweet_count = Column(Integer, nullable=False)
    tweet_count = Column(Integer, nullable=False)

    @hybrid_property
    def total_count(self) -> int:
        return (
            self.like_count
            + self.quote_count
            + self.reply_count
            + self.retweet_count
            + self.tweet_count
        )


class Prediction(BaseMixin, Base):
    __tablename__ = "prediction"
    __table_args__ = (
        UniqueConstraint('user_id', 'celebrity_id', 'metric'),
    )

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    celebrity_id = Column(Integer, ForeignKey("celebrity.id", ondelete="CASCADE"), nullable=False)

    is_enabled = Column(Boolean, default=True, nullable=False)
    is_auto_disabled = Column(Boolean, default=False, nullable=False)
    amount = Column(Integer, nullable=False)

    # like, retweet, reply, quote
    metric = Column(String(20), nullable=False)

    def __repr__(self) -> str:
        return f"user:{self.user_id} celebrity:{self.celebrity_id} amount:{self.amount} ({self.id})"


class PredictionResult(BaseMixin, Base):
    # Note: these are created at scoring time and are not related to Prediction
    # since those can change or be deleted.
    __tablename__ = "prediction_result"
    __table_args__ = (
        UniqueConstraint('user_id', 'celebrity_id', 'metric', 'metric_date'),
    )

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    celebrity_id = Column(Integer, ForeignKey("celebrity.id", ondelete="CASCADE"), nullable=False)

    metric_date = Column(Date, nullable=False)
    amount = Column(Integer, nullable=False)
    metric = Column(String(20), nullable=False)

    # These will start as null since we are creating these rows the day before scoring.
    actual = Column(Integer)
    points = Column(Integer)
