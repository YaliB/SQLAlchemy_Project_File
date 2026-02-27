from sqlalchemy.orm import Session
from sqlalchemy import func
from . import db_models # Using naming convention for models

# 1. Top 5 Most Liked Posts (JOIN + GROUP BY)
def get_top_liked_posts(db: Session):
    # Joins Posts with Likes to count popularity
    return db.query(
        db_models.Post.title,
        func.count(db_models.Like.id).label("likes_count")
    ).join(db_models.Like).group_by(db_models.Post.id).order_by(func.count(db_models.Like.id).desc()).limit(5).all()

# 2. Most Active Users by Post Count (JOIN + GROUP BY)
def get_most_active_users(db: Session):
    # Joins Users with Posts to see who writes the most
    return db.query(
        db_models.User.name,
        func.count(db_models.Post.id).label("post_count")
    ).join(db_models.Post).group_by(db_models.User.id).order_by(func.count(db_models.Post.id).desc()).limit(5).all()

# 3. Groups with the most members (JOIN + GROUP BY)
def get_popular_groups(db: Session):
    # Joins Groups with Memberships to find largest communities
    return db.query(
        db_models.Group.name,
        func.count(db_models.GroupMembership.user_id).label("member_count")
    ).join(db_models.GroupMembership).group_by(db_models.Group.id).order_by(func.count(db_models.GroupMembership.user_id).desc()).all()

# 4. Users who have never posted anything (LEFT OUTER JOIN)
def get_silent_users(db: Session):
    # Finds users that exist in Users table but NOT in Posts table
    return db.query(db_models.User.name).outerjoin(db_models.Post).filter(db_models.Post.id == None).all()

# 5. Average comments per post (Aggregate query)
def get_avg_comments_per_post(db: Session):
    # Subquery/Count to get stats on user engagement
    subquery = db.query(
        func.count(db_models.Comment.id).label("count")
    ).group_by(db_models.Comment.post_id).subquery()
    
    return db.query(func.avg(subquery.c.count)).scalar()