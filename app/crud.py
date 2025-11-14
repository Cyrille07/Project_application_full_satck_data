from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException, status

# User CRUD
def create_user(db: Session, user: schemas.UserCreate):
    db_query_exist_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if db_query_exist_user :
        raise HTTPException(status_code=404, detail="User with this email already exist")

    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()



# BlogPost CRUD
def create_blogpost(db: Session, post: schemas.BlogPostCreate, user_id: int):
    existing_post = db.query(models.BlogPost).filter( models.BlogPost.title == post.title).first()

    if existing_post :
        raise HTTPException(status_code=404, detail="A post with this title already exist")

    db_post = models.BlogPost(**post.dict(), author_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_blogposts(db: Session):
    return db.query(models.BlogPost).all()

def get_blogposts_specific(db: Session, user_id: id):
    return db.query(models.BlogPost).filter(models.BlogPost.author_id == user_id ).first()


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


# Comments_Posts CRUD
def create_comment_posts(db: Session, comment: schemas.Comments_PostCreate, user_id, post_id):
    db_comment = models.Comments_Post(**comment.dict(), author_id=user_id, blogpost_linked_id=post_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_posts(db: Session):
    return db.query(models.Comments_Post).all()

def update_comments_post(db: Session, comment: schemas.Comments_PostCreate, comment_id: int, user_id : int):
    db_comment= db.query(models.Comments_Post).filter(models.Comments_Post.id==comment_id).first()

    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if db_comment.author_id != user_id:
        raise HTTPException(403, "You cannot update a comment you do not own")
    
    if db_comment.author_id == user_id: 
        db_comment.content = comment.content
        db.commit()
        db.refresh(db_comment)
    return db_comment




