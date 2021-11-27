from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional


class OrmBaseType(BaseModel):
    class Config:
        orm_mode = True


class TokenType(BaseModel):
    access_token: str
    token_type: str


class UserBaseType(OrmBaseType):
    username: str
    created_at: Optional[datetime] = None


class UserCreateType(UserBaseType):
    email_address: str
    password: str


class UserUpdateType(UserBaseType):
    email_address: str
    password: Optional[str] = None


class CurrentUserType(UserBaseType):
    email_address: str


class CelebrityCreateType(OrmBaseType):
    twitter_username: str
    twitter_name: Optional[str] = None
    twitter_description: Optional[str] = None
    twitter_verified: Optional[bool] = False
    twitter_profile_image_url: Optional[str] = None


class CelebrityType(CelebrityCreateType):
    id: int
    tweets: Optional[list] = []
    metrics: Optional[list] = []


class PredictionBaseType(OrmBaseType):
    celebrity_id: int
    is_enabled: bool
    is_auto_disabled: bool
    amount: int
    metric: str


class PredictionCreateType(PredictionBaseType):
    user_id: int


class PredictionType(PredictionCreateType):
    id: int
    celebrity: Optional[CelebrityType] = None


class PredictionUpdateType(OrmBaseType):
    is_enabled: Optional[bool]
    is_auto_disabled: Optional[bool]
    amount: Optional[int]
    metric: Optional[str]


class CelebrityDailyMetricsCreateType(OrmBaseType):
    celebrity_id: int
    metric_date: date
    like_count: int
    quote_count: int
    reply_count: int
    retweet_count: int
    tweet_count: int


class CelebrityDailyMetricsType(CelebrityDailyMetricsCreateType):
    id: int
    total_count: Optional[int]


class PredictionResultCreateType(OrmBaseType):
    user_id: int
    celebrity_id: int
    amount: int
    metric: str
    metric_date: date
    points: Optional[int] = None


class PredictionResultType(PredictionResultCreateType):
    id: int
    celebrity: Optional[CelebrityCreateType] = None

    # The metric amount as of now.
    current: Optional[int] = 0
