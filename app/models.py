from datetime import datetime
from flask_sqlalchemy import Model

from .db import db


class BaseModel(Model):
    id = db.Column(db.Integer(), primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow())
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow())

    def save(self) -> None:
        if not self.id:
            db.session.add(self)

        db.session.commit()


class User(BaseModel, db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_staff = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def is_anonymous(self) -> bool:
        return False

    def get_id(self) -> str:
        return self.id


class Celebrity(BaseModel, db.Model):
    twitter_username = db.Column(db.String(100), unique=True, nullable=False)

    # These are nullable because we will start with their username and then fetch the rest.
    twitter_id = db.Column(db.BigInteger(), unique=True)
    twitter_name = db.Column(db.String(100))


# from datetime import datetime
# from sqlalchemy import Table, Column, DateTime, Integer, String, Boolean, BigInteger
# from sqlalchemy.ext.declarative import declarative_base, declared_attr, DeclarativeMeta

# Base: DeclarativeMeta = declarative_base()

# # from .db import meta


# class BaseMixin:
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()

#     id = Column(Integer, primary_key=True)
#     created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
#     updated_at = Column(DateTime, onupdate=datetime.utcnow())


# class User(BaseMixin, Base):
#     username = Column(String(20), unique=True, nullable=False)
#     password = Column(String(200), nullable=False)
#     email_address = Column(String(120), unique=True, nullable=False)
#     is_active = Column(Boolean, default=True, nullable=False)
#     is_staff = Column(Boolean, default=False, nullable=False)


# class Celebrity(BaseMixin, Base):
#     twitter_username = Column(String(100), unique=True, nullable=False)

#     # These are nullable because we will start with their username and then fetch the rest.
#     twitter_id = Column(BigInteger(), unique=True)
#     twitter_name = Column(String(100))
