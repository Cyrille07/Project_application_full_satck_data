from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas, database

router = APIRouter(prefix="/posts", tags=["blogposts"])

@router.post("/", response_model=schemas.BlogPost)
def create_post(post: schemas.BlogPostCreate, db: Session = Depends(database.get_db)):
    return crud.create_blogpost(db, post, user_id=4)  # TODO: lier avec authentification

@router.get("/", response_model=list[schemas.BlogPost])
def read_posts(db: Session = Depends(database.get_db)):
    return crud.get_blogposts(db)

@router.put("/", response_model=schemas.BlogPost)
def update_post_by_user(post: schemas.BlogPostCreate, db: Session = Depends(database.get_db)):
    return crud.update_blogpost(db, post, post_id=2, user_id=2)

@router.get("/{id}", response_model=list[schemas.BlogPost])
def read_specific_post(id: int, db: Session = Depends(database.get_db) ):
    return crud.get_blogposts_specific(id,db)