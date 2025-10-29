from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class BlogPostBase(BaseModel):
    title: str
    content: str

class BlogPostCreate(BlogPostBase):
    pass

class BlogPost(BlogPostBase):
    id: int
    created_at: datetime
    author_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    posts: List[BlogPost] = []

    class Config:
        orm_mode = True