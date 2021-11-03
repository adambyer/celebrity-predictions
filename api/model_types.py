from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True


class TokenType(BaseModel):
    access_token: str
    token_type: str


class UserBaseType(OrmBaseModel):
    username: str


class UserCreateType(UserBaseType):
    email_address: str
    password: str


class UserType(UserBaseType):
    created_at: datetime


class CurrentUserType(UserType):
    email_address: str


class CelebrityType(OrmBaseModel):
    id: int
    twitter_username: str
    twitter_name: Optional[str] = None
    twitter_description: Optional[str] = None
    twitter_verified: Optional[bool] = False
    twitter_profile_image_url: Optional[str] = None
    tweets: Optional[list] = []


class PredictionBaseType(OrmBaseModel):
    celebrity_id: int
    is_enabled: bool
    is_auto_disabled: bool
    amount: int


class PredictionCreateType(PredictionBaseType):
    user_id: int


class PredictionType(PredictionCreateType):
    id: int


class CelebrityDailyMetricCreateType(OrmBaseModel):
    celebrity_id: int
    metric_date: date
    metric: str
    amount: int


class CelebrityDailyMetricType(CelebrityDailyMetricCreateType):
    id: int


class PredictionResultCreateType(OrmBaseModel):
    user_id: int
    celebrity_id: int
    amount: int
    metric: str
    metric_date: date
    points: int


class PredictionResultType(PredictionResultCreateType):
    id: int
