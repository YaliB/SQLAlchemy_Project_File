from sqlalchemy.orm import Session
from ..db_models import GroupMembership, User, Group
from .. import api_models

# Add a user to a group (Create Membership)
def add_user_to_group(db: Session, membership: api_models.GroupMembershipCreate):
    db_membership = GroupMembership(
        user_id=membership.user_id,
        group_id=membership.group_id,
    )
    db.add(db_membership)
    db.commit()
    db.refresh(db_membership)
    return db_membership

# Get all members of a specific group (JOIN with User table)
def get_group_members(db: Session, group_id: int):
    return db.query(User).join(GroupMembership).filter(
        GroupMembership.group_id == group_id
    ).all()

# Get all groups a specific user belongs to (JOIN with Group table)
def get_user_groups(db: Session, user_id: int):
    return db.query(Group).join(GroupMembership).filter(
        GroupMembership.user_id == user_id
    ).all()

# Remove a user from a group (Delete Membership)
def remove_user_from_group(db: Session, user_id: int, group_id: int):
    db_membership = db.query(GroupMembership).filter(
        GroupMembership.user_id == user_id,
        GroupMembership.group_id == group_id
    ).first()
    
    if db_membership:
        db.delete(db_membership)
        db.commit()
        return True
    return 


def get_membership_by_user_and_group(db: Session, user_id: int, group_id: int):
    return db.query(GroupMembership).filter(
        GroupMembership.user_id == user_id,
        GroupMembership.group_id == group_id
    ).first()