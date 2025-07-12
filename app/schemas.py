from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(Post):
    pass


class UserCreate(BaseModel):
    name: str
    password: str
    email: EmailStr


class UserOut(BaseModel):
    name: str
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ResponsePost(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    post: ResponsePost
    vote_count: int

    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
