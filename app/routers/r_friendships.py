from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import api_models
from ..crud import crud_friendships

router = APIRouter()

# CREATE - Create a new friendship
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_friend(friendship: api_models.FriendshipCreate, db: Session = Depends(get_db)):
    # Creates a friendship link between two users
    return crud_friendships.create_friendship(db, friendship)

# READ - List all friendships for a user
@router.get("/user/{user_id}")
def list_friends(user_id: int, db: Session = Depends(get_db)):
    # Returns friendship records for a user
    return crud_friendships.get_user_friends(db, user_id)

# delete a friendship
@router.delete("/{friendship_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_friendship(friendship_id: int, db: Session = Depends(get_db)):
    return crud_friendships.delete_friendship(db, friendship_id)
