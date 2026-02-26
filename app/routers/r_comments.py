from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import api_models
from ..crud import crud_comments

router = APIRouter()

# CREATE - Create a new comment
@router.post("/", response_model=api_models.CommentResponse, status_code=status.HTTP_201_CREATED)
def post_comment(comment: api_models.CommentCreate, db: Session = Depends(get_db)):
    # Links a user to a post with a text content
    return crud_comments.create_comment(db=db, comment=comment)

# READ - Get all comments
@router.get("/post/{post_id}", response_model=List[api_models.CommentResponse])
def get_post_comments(post_id: int, db: Session = Depends(get_db)):
    # Returns all comments for a specific post
    return crud_comments.get_comments_by_post(db, post_id=post_id)

# READ - Get a specific comment
@router.get("/{comment_id}", response_model=api_models.CommentResponse)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    return crud_comments.get_comment_by_id(db, comment_id)

# UPDATE - Update an existing comment
@router.put("/{comment_id}", response_model=api_models.CommentResponse)
def update_comment(comment_id: int, comment: api_models.CommentCreate, db: Session = Depends(get_db)):
    return crud_comments.update_comment(db=db, comment_id=comment_id, comment_data=comment)

# DELETE - Delete an existing comment
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    return crud_comments.delete_comment(db=db, comment_id=comment_id)

# READ - Get all comments for a specific user
@router.get("/user/{user_id}", response_model=List[api_models.CommentResponse])
def get_user_comments(user_id: int, db: Session = Depends(get_db)):
    return crud_comments.get_comments_by_user(db, user_id=user_id)

