from sqlalchemy import func
from .db import db_session  # Import the context manager
from . import db_models

# 1. Top 5 Most Liked Posts (JOIN + GROUP BY)
def get_top_liked_posts():
    with db_session() as db:
        return db.query(
            db_models.Post.title,
            func.count(db_models.Like.id).label("likes_count")
        ).join(db_models.Like).group_by(db_models.Post.id).order_by(func.count(db_models.Like.id).desc()).limit(5).all()

# 2. Most Active Users by Post Count (JOIN + GROUP BY)
def get_most_active_users():
    with db_session() as db:
        return db.query(
            db_models.User.name,
            func.count(db_models.Post.id).label("post_count")
        ).join(db_models.Post).group_by(db_models.User.id).order_by(func.count(db_models.Post.id).desc()).limit(5).all()

# 3. Groups with the most members (JOIN + GROUP BY)
def get_popular_groups():
    with db_session() as db:
        return db.query(
            db_models.Group.name,
            func.count(db_models.GroupMembership.user_id).label("member_count")
        ).join(db_models.GroupMembership).group_by(db_models.Group.id).order_by(func.count(db_models.GroupMembership.user_id).desc()).all()

# 4. Users who have never posted anything (LEFT OUTER JOIN)
def get_silent_users():
    with db_session() as db:
        return db.query(db_models.User.name).outerjoin(db_models.Post).filter(db_models.Post.id == None).all()

# 5. Average comments per post (Aggregate query)
def get_avg_comments_per_post():
    with db_session() as db:
        subquery = db.query(
            func.count(db_models.Comment.id).label("count")
        ).group_by(db_models.Comment.post_id).subquery()
        
        result = db.query(func.avg(subquery.c.count)).scalar()
        return result if result else 0