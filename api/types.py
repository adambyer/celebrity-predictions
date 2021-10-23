from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class UserBaseType(BaseModel):
    username: str
    email_address: str

    class Config:
        orm_mode = True


class UserCreateType(UserBaseType):
    password: str


class UserType(UserBaseType):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class CelebrityBaseType(BaseModel):
    twitter_username: str
    twitter_id: Optional[int] = None
    twitter_name: Optional[str] = None

    class Config:
        orm_mode = True


class CelebrityType(CelebrityBaseType):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
