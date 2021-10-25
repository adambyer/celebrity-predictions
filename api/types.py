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


class CelebrityType(BaseModel):
    twitter_username: str
    twitter_name: Optional[str] = None
    twitter_description: Optional[str] = None
    twitter_verified: Optional[bool] = False
    twitter_profile_image_url: Optional[str] = None
    tweets: Optional[list] = []

    class Config:
        orm_mode = True
