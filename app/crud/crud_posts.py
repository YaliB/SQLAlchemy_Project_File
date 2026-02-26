from sqlalchemy.orm import Session
from ..db_models import Post 
from .. import api_models

# Get a single post by its ID
def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

# Get a list of posts with pagination
def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()

# Get all posts belonging to a specific user
def get_user_posts(db: Session, user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).all()

# Create a new post linked to a user
def create_post(db: Session, post: api_models.PostCreate):
    db_post = Post(
        title=post.title,
        content=post.content,
        user_id=post.user_id  # Foreign Key link
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Update post content or title
def update_post(db: Session, post_id: int, post_data: api_models.PostCreate):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db_post.title = post_data.title
        db_post.content = post_data.content
        db.commit()
        db.refresh(db_post)
    return db_post

# Delete a post
def delete_post(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
        return True
    return False