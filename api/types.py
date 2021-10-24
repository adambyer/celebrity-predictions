from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TokenType(BaseModel):
    access_token: str
    token_type: str


class UserBaseType(BaseModel):
    username: str

    class Config:
        orm_mode = True


class UserCreateType(UserBaseType):
    email_address: str
    password: str


class UserType(UserBaseType):
    created_at: datetime


class CurrentUserType(UserType):
    email_address: str


class CelebrityBaseType(BaseModel):
    twitter_username: str
    twitter_id: Optional[int] = None
    twitter_name: Optional[str] = None

    class Config:
        orm_mode = True


class CelebrityType(CelebrityBaseType):
    created_at: datetime
    updated_at: Optional[datetime] = None
