from sqlalchemy.orm import Session
from ..db_models import Comment
from .. import api_models

# Create a new comment
def create_comment(db: Session, comment: api_models.CommentCreate):
    db_comment = Comment(
        content=comment.content,
        user_id=comment.user_id,
        post_id=comment.post_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


# Get a specific comment
def get_comment_by_id(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

# Get all comments for a specific post
def get_comments_by_post(db: Session, post_id: int):
    # Returns all comments for a specific post
    return db.query(Comment).filter(Comment.post_id == post_id).all()

# Get all comments for a specific user
def get_comments_by_user(db: Session, user_id: int):
    # Returns all comments for a specific user
    return db.query(Comment).filter(Comment.user_id == user_id).all()

# Update a specific comment
def update_comment(db: Session, comment_id: int, comment_data: api_models.CommentCreate):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db_comment.content = comment_data.content
        db.commit()
        db.refresh(db_comment)
    return db_comment

# Delete a specific comment
def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()
        return True
    return False
