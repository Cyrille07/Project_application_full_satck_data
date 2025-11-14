from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud, schemas, database

router = APIRouter(prefix="/commentspost", tags=["comments"])

@router.post("/", response_model=schemas.Comments_Post)
def create_comment_post(comment: schemas.Comments_PostCreate, db: Session = Depends(database.get_db)):
    return crud.create_comment_posts(db, comment, user_id=1, post_id=2)

@router.get("/", response_model=list[schemas.Comments_Post])
def read_users(db: Session = Depends(database.get_db)):
    return crud.get_comments_posts(db)