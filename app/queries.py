from sqlalchemy import select, func

from db import Session
from models import User


def select_user(session: Session):
    stmt = (
        select(User.id, User.name, func.count(User.id).label("userCount"))
    )
    
    rows = session.execute(stmt).all()


#################################################################################################################################

from fastapi import APIRouter, Depends
from sqlalchemy import func
from db import get_db
from models import models

router = APIRouter()

@router.get("/popular-posts")
def get_popular_posts(db: Session = Depends(get_db)):
    # Join Posts with Likes and count occurrences
    results = db.query(
        models.Post.title, 
        func.count(models.Like.id).label("total_likes")
    ).join(models.Like, models.Post.id == models.Like.post_id) \
     .group_by(models.Post.id) \
     .order_by(func.count(models.Like.id).desc()) \
     .limit(5).all()
    
    return [{"title": r[0], "likes": r[1]} for r in results]


@router.get("/active-users")
def get_active_users(db: Session = Depends(get_db)):
    # Join Users with Posts to find who publishes the most
    results = db.query(
        models.User.name, 
        func.count(models.Post.id).label("post_count")
    ).join(models.Post, models.User.id == models.Post.user_id) \
     .group_by(models.User.id) \
     .order_by(func.count(models.Post.id).desc()) \
     .all()
    
    return [{"user": r[0], "posts": r[1]} for r in results]


@router.get("/group-stats")
def get_group_stats(db: Session = Depends(get_db)):
    # Count members for each group using the Bridge Table
    results = db.query(
        models.Group.name, 
        func.count(models.GroupMembership.user_id).label("member_count")
    ).join(models.GroupMembership, models.Group.id == models.GroupMembership.group_id) \
     .group_by(models.Group.id).all()
    
    return [{"group": r[0], "members": r[1]} for r in results]


@router.get("/inactive-users")
def get_inactive_users(db: Session = Depends(get_db)):
    # Find users who have 0 posts using an Outer Join
    results = db.query(models.User.name) \
        .outerjoin(models.Post) \
        .filter(models.Post.id == None).all()
    return [r[0] for r in results]