from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = "postgresql://localhost/celebrity_predictions"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
Base: DeclarativeMeta = declarative_base()
