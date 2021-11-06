from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Generator

from ..constants import JWT_ALGORITHM, JWT_SECRET_KEY
from ..crud import get_user_by_username
from ..db import Session
from ..models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db() -> Generator:
    """Get database dependency."""
    db = Session()
    try:
        yield db
    finally:
        db.close()


# TODO: why is this async?
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("sub")
        expires = payload.get("exp")

        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if not expires or datetime.utcnow() > expires:
        raise credentials_exception

    user = get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception

    return user
