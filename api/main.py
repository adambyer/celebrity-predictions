from fastapi import Depends, FastAPI, HTTPException
from typing import List

from . import crud
from .db import Session
from .types import UserType, UserCreateType
app = FastAPI()


# Database dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/", response_model=UserType)
def create_user(user: UserCreateType, db: Session = Depends(get_db)):
    is_user_taken = crud.user_taken(user.username, user.email_address)
    if is_user_taken:
        raise HTTPException(status_code=400, detail="Email address or username already registered.")
    return crud.create_user(db=db, user=user)


@app.get("/user/", response_model=List[UserType])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/user/{user_id}", response_model=UserType)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return db_user
