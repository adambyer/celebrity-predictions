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
    id: int
    twitter_username: str
    twitter_name: Optional[str] = None
    twitter_description: Optional[str] = None
    twitter_verified: Optional[bool] = False
    twitter_profile_image_url: Optional[str] = None
    tweets: Optional[list] = []

    class Config:
        orm_mode = True


class PredictionBaseType(BaseModel):
    celebrity_id: int
    is_enabled: bool
    is_auto_disabled: bool
    amount: int

    class Config:
        orm_mode = True


class PredictionCreateType(PredictionBaseType):
    user_id: int


class PredictionType(PredictionCreateType):
    id: int


class PredictionResultType(BaseModel):
    id: int
    prediction_id: int
    amount: int
    points: int

    class Config:
        orm_mode = True
