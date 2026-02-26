from sqlalchemy.orm import Session
from ..db_models import Friendship
from .. import api_models

# Create a new friendship
def create_friendship(db: Session, friendship: api_models.FriendshipCreate):
    db_friendship = Friendship(
        user_id=friendship.user_id,
        friend_id=friendship.friend_id
    )
    db.add(db_friendship)
    db.commit()
    db.refresh(db_friendship)
    return db_friendship

# Get all friends of a user
def get_user_friends(db: Session, user_id: int):
    # Simple query to find all friends of a user
    return db.query(Friendship).filter(Friendship.user_id == user_id).all()


# Update a friendship
def update_friendship(db: Session, friendship_id: int, friendship: api_models.FriendshipCreate):
    db_friendship = db.query(Friendship).filter(Friendship.id == friendship_id).first()
    if db_friendship:
        db_friendship.user_id = friendship.user_id
        db_friendship.friend_id = friendship.friend_id
        db.commit()
        db.refresh(db_friendship)
    return db_friendship

# Delete a friendship
def delete_friendship(db: Session, friendship_id: int):
    db_friendship = db.query(Friendship).filter(Friendship.id == friendship_id).first()
    if db_friendship:
        db.delete(db_friendship)
        db.commit()
        return True
    return False

# Get a specific friendship
def get_friendship(db: Session, friendship_id: int):
    return db.query(Friendship).filter(Friendship.id == friendship_id).first()

