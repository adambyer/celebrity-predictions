from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, Boolean, BigInteger

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


class Celebrity(BaseMixin, Base):
    __tablename__ = "celebrity"

    twitter_username = Column(String(100), unique=True, nullable=False)
    twitter_verified = Column(Boolean, default=False, nullable=False)

    # These are nullable because we will start with their username and then fetch the rest.
    twitter_id = Column(BigInteger(), unique=True)
    twitter_name = Column(String(100))
    twitter_profile_image_url = Column(String(1000))
    twitter_description = Column(String(1000))
