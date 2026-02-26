from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from .. import api_models
from ..crud import crud_likes

router = APIRouter()

# CREATE - Create a new like
@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(like: api_models.LikeCreate, db: Session = Depends(get_db)):
    # Adds a like record to the bridge table
    return crud_likes.add_like(db=db, like=like)

# DELETE - Remove a like
@router.delete("/{post_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def unlike_post(post_id: int, user_id: int, db: Session = Depends(get_db)):
    success = crud_likes.remove_like(db, user_id=user_id, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Like not found")
    return None

# READ - Get all likes for a post
@router.get("/post/{post_id}", response_model=List[api_models.LikeResponse])
def get_post_likes(post_id: int, db: Session = Depends(get_db)):
    return crud_likes.get_likes_by_post(db, post_id=post_id)

# READ - Get all likes for a user
@router.get("/user/{user_id}", response_model=List[api_models.LikeResponse])
def get_user_likes(user_id: int, db: Session = Depends(get_db)):
    return crud_likes.get_likes_by_user(db, user_id=user_id)

