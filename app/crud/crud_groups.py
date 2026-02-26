from sqlalchemy.orm import Session
from ..db_models import Group
from .. import api_models

# Get a single group
def get_group(db: Session, group_id: int):
    return db.query(Group).filter(Group.id == group_id).first()

# Get all groups
def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Group).offset(skip).limit(limit).all()

# Create a new group
def create_group(db: Session, group: api_models.GroupCreate):
    db_group = Group(name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

# Update a group
def update_group(db: Session, group_id: int, group: api_models.GroupCreate):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group:
        db_group.name = group.name
        db.commit()
        db.refresh(db_group)
    return db_group

# Delete a group
def delete_group(db: Session, group_id: int):
    db_group = db.query(Group).filter(Group.id == group_id).first()
    if db_group:
        db.delete(db_group)
        db.commit()
        return True
    return False