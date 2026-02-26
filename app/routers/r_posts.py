from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import api_models
from ..crud import crud_posts, crud_users

router = APIRouter()

# CREATE - Create a new post
@router.post("/", response_model=api_models.PostResponse, status_code=status.HTTP_201_CREATED)
def create_new_post(post: api_models.PostCreate, db: Session = Depends(get_db)):
    """
    Create a post linked to a user_id. 
    Note: Ensure user_id exists in the users table first.
    """
    if not crud_users.get_user_by_id(db, user_id=post.user_id):
        raise HTTPException(status_code=404, detail="User not found") 
    return crud_posts.create_post(db=db, post=post)

# READ ALL - Get all posts with pagination
@router.get("/", response_model=List[api_models.PostResponse])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve posts with optional pagination (skip and limit).
    """
    posts = crud_posts.get_posts(db, skip=skip, limit=limit)
    return posts

# READ ONE - Get a specific post by ID
@router.get("/{post_id}", response_model=api_models.PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = crud_posts.get_post_by_id(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# UPDATE - Update an existing post
@router.put("/{post_id}", response_model=api_models.PostResponse)
def update_existing_post(post_id: int, post: api_models.PostCreate, db: Session = Depends(get_db)):
    if not crud_users.get_user_by_id(db, user_id=post.user_id):
        raise HTTPException(status_code=404, detail="User not found") 
    db_post = crud_posts.update_post(db=db, post_id=post_id, post_data=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

# DELETE - Remove a post
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_post(post_id: int, db: Session = Depends(get_db)):
    success = crud_posts.delete_post(db=db, post_id=post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return None