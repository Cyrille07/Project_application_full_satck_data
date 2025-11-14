from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comments_Post",back_populates="author")

class BlogPost(Base):
    __tablename__ = "blogposts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True,index=True, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
    comments = relationship("Comments_Post", back_populates="post_commented")

class Comments_Post(Base):
    __tablename__ = "commentspost"

    id = Column(Integer, primary_key=True, index= True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    author_id = Column(Integer, ForeignKey("users.id"))
    blogpost_linked_id = Column(Integer, ForeignKey("blogposts.id"))

    author = relationship("User", back_populates="comments")
    post_commented = relationship("BlogPost", back_populates="comments")


