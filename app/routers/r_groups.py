from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import api_models
from ..crud import crud_groups  

router = APIRouter()

# CREATE - Create a new group
@router.post("/", response_model=api_models.GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(group: api_models.GroupCreate, db: Session = Depends(get_db)):
    # Standard group creation
    return crud_groups.create_group(db=db, group=group)

# READ - Get a single group
@router.get("/{group_id}", response_model=api_models.GroupResponse)
def read_group(group_id: int, db: Session = Depends(get_db)):
    db_group = crud_groups.get_group(db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return db_group

# READ - Get all groups
@router.get("/", response_model=List[api_models.GroupResponse])
def read_groups(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_groups.get_groups(db, skip=skip, limit=limit)

# UPDATE - Update an existing group
@router.put("/{group_id}", response_model=api_models.GroupResponse)
def update_group(group_id: int, group: api_models.GroupCreate, db: Session = Depends(get_db)):
    db_group = crud_groups.get_group(db, group_id=group_id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Group not found")
    return crud_groups.update_group(db=db, group_id=group_id, group=group)

# DELETE - Delete a group
@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: int, db: Session = Depends(get_db)):
    success = crud_groups.delete_group(db=db, group_id=group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Group not found")
    return None

# READ - Get all users in a group
@router.get("/{group_id}/users", response_model=List[api_models.UserResponse])
def read_group_members(group_id: int, db: Session = Depends(get_db)):
    return crud_groups.get_group_members(db, group_id)

# READ - Get all groups a user is a member of
@router.get("/user/{user_id}", response_model=List[api_models.GroupResponse])
def read_user_groups(user_id: int, db: Session = Depends(get_db)):
    return crud_groups.get_user_groups(db, user_id)
