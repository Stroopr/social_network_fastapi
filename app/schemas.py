from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    username: str
    password: str


class UserCreate(UserBase):
    pass


class UserCreateResponse(BaseModel):
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserGetResponse(BaseModel):
    email: EmailStr
    username: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    created_at: datetime
    id: int
    owner_id: int
    owner: UserGetResponse

    class Config:
        orm_mode = True


class PostVoteResponse(BaseModel):
    Post:PostResponse
    votes:int


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
