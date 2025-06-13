from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class ResponsePost(Post):
    id: int
    created_at: datetime
    owner_id: int
    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    name: str
    password: str
    email: EmailStr

class UserOut(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr
    name: str
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
