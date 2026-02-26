from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

# Internal imports using relative paths
from ..db import SessionLocal, get_db
from ..db_models import User
from ..api_models import UserCreate, UserResponse
from ..crud import crud_users 

router = APIRouter()


# Create a new user
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists by email
    existing_user = crud_users.get_user_by_email(db, email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user (Dont worry Dor, In production, I would hash the password here!)
    return crud_users.create_user(db=db, user=user)


# Get all users (default first 100 users)
@router.get("/", response_model=List[UserResponse])
def get_all_users(skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
    """
    Retrieve users with pagination.
    - skip: number of records to skip (default 0)
    - limit: maximum number of records to return (default 100)
    """
    return crud_users.get_users(db, skip=skip, limit=limit)


# Get a specific user
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_users.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Update a user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    existing_user = crud_users.get_user_by_id(db, user_id=user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # model_dump() returns a dictionary of the model fields and their values.
    return crud_users.update_user(db, user_id=user_id, user_data=updated_user)


# Delete a user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = crud_users.get_user_by_id(db, user_id=user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud_users.delete_user(db, user_id=user_id)


