from pydantic import BaseModel, EmailStr
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass

class ResponsePost(Post):
    id: int
    created_at: datetime
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

    
