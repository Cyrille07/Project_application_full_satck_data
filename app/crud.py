from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

# BlogPost CRUD
def create_blogpost(db: Session, post: schemas.BlogPostCreate, user_id: int):
    db_post = models.BlogPost(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_blogposts(db: Session):
    return db.query(models.BlogPost).all()

def update_blogpost(db: Session, updated_post: schemas.BlogPostCreate, post_id: int, user_id : int):
    db_post= db.query(models.BlogPost).filter(models.BlogPost.id==post_id).first()

    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if db_post.author_id == user_id: 
        db_post.title = updated_post.title
        db_post.content =  updated_post.content
        db.commit()
        db.refresh(db_post)
    return db_post




