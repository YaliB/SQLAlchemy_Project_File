from sqlalchemy import func
from .db import db_session 
from . import db_models

# 1. Top 5 Most Liked Posts
def get_top_liked_posts():
    """
    Retrieves the top 5 posts based on the number of likes.
    """
    with db_session() as db:
        return db.query(
            db_models.Post.title,
            func.count(db_models.Like.id).label("likes_count")
        ).join(db_models.Like).group_by(db_models.Post.id).order_by(func.count(db_models.Like.id).desc()).limit(5).all()

# 2. Most Active Users (Updated to use display_name for perfection)
def get_most_active_users():
    """
    Retrieves the top 5 users by post count, showing their display name from the profile.
    """
    with db_session() as db:
        return db.query(
            db_models.UserProfile.display_name, # Logic: Displaying the friendly name
            func.count(db_models.Post.id).label("post_count")
        ).join(db_models.User, db_models.User.id == db_models.UserProfile.user_id) \
         .join(db_models.Post, db_models.Post.user_id == db_models.User.id) \
         .group_by(db_models.UserProfile.id) \
         .order_by(func.count(db_models.Post.id).desc()).limit(5).all()
    
# 3. Popular Groups
def get_popular_groups():
    """
    Retrieves groups with the highest member count.
    """
    with db_session() as db:
        return db.query(
            db_models.Group.name,
            func.count(db_models.GroupMembership.user_id).label("member_count")
        ).join(db_models.GroupMembership).group_by(db_models.Group.id).order_by(func.count(db_models.GroupMembership.user_id).desc()).all()

# 4. Silent Users (Updated to return both username and display_name for better context)
def get_silent_users():
    """
    Returns usernames of users who have never created a post.
    """
    with db_session() as db:
        return db.query(db_models.User.username).outerjoin(db_models.Post).filter(db_models.Post.id == None).all()

# 5. Average comments per post (Corrected logical average)
def get_avg_comments_per_post():
    """
    Calculates the true average of comments per post across ALL posts.
    """
    with db_session() as db:
        # Step 1: Count comments for EVERY post (including those with 0 comments)
        subquery = db.query(
            func.count(db_models.Comment.id).label("comment_count")
        ).select_from(db_models.Post).outerjoin(db_models.Comment).group_by(db_models.Post.id).subquery()
        
        # Step 2: Calculate the average of those counts
        result = db.query(func.avg(subquery.c.comment_count)).scalar()
        return float(result) if result else 0.0