from sqlalchemy.orm import Session
from ..db_models import Like
from .. import api_models

# Create a new like
def add_like(db: Session, like: api_models.LikeCreate):
    # Check if like already exists to prevent duplicates
    existing_like = db.query(Like).filter(
        Like.user_id == like.user_id,
        Like.post_id == like.post_id
    ).first()
    
    if existing_like:
        return existing_like
        
    db_like = Like(user_id=like.user_id, post_id=like.post_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like

# Remove a like
def remove_like(db: Session, user_id: int, post_id: int):
    db_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()
    if db_like:
        db.delete(db_like)
        db.commit()
        return True
    return False


# -- For Statistics -- 
# Get all likes for a specific post
def get_likes_by_post(db: Session, post_id: int):
    return db.query(Like).filter(Like.post_id == post_id).all()

# Get all likes for a specific user
def get_likes_by_user(db: Session, user_id: int):
    return db.query(Like).filter(Like.user_id == user_id).all()