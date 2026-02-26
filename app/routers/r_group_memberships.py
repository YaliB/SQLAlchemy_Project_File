from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_db
from .. import api_models
from ..crud import crud_group_memberships

router = APIRouter()

# POST: Join a group
@router.post("/", response_model=api_models.GroupMembershipResponse)
def join_group(membership: api_models.GroupMembershipCreate, db: Session = Depends(get_db)):

    if crud_group_memberships.get_membership_by_user_and_group(db, membership.user_id, membership.group_id):
        raise HTTPException(status_code=400, detail="User is already a member of this group")

    return crud_group_memberships.add_user_to_group(db, membership)

# GET: List all members in a group
@router.get("/group/{group_id}")
def read_group_members(group_id: int, db: Session = Depends(get_db)):
    return crud_group_memberships.get_group_members(db, group_id)

# DELETE: Leave a group
@router.delete("/{group_id}/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def leave_group(group_id: int, user_id: int, db: Session = Depends(get_db)):
    success = crud_group_memberships.remove_user_from_group(db, user_id, group_id)
    if not success:
        raise HTTPException(status_code=404, detail="Membership not found")
    return None