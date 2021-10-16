from datetime import datetime
from flask_sqlalchemy import Model
from sqlalchemy import Column, DateTime, Integer

from .db import db


class BaseModel(Model):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, onupdate=datetime.utcnow())


class User(BaseModel, db.Model):
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
