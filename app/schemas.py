from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class Comments_PostBase(BaseModel):
    content : str

class Comments_PostCreate(Comments_PostBase):
    pass

class Comments_Post(Comments_PostBase):
    id : int 
    created_at: datetime
    author_id: int
    blogpost_linked_id: int

    class Config:
        orm_mode = True


#-------------------------------------------------------------


class BlogPostBase(BaseModel):
    title: str
    content: str

class BlogPostCreate(BlogPostBase):
    pass

class BlogPost(BlogPostBase):
    id: int
    created_at: datetime
    author_id: int
    comments : List[Comments_Post] = []

    class Config:
        orm_mode = True



#-------------------------------------------------------------


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    posts: List[BlogPost] = []
    comments: List[Comments_Post] = []

    class Config:
        orm_mode = True




