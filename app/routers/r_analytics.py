from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import queries

router = APIRouter()

@router.get("/top-posts")
def top_posts(db: Session = Depends(get_db)):
    """Get the 5 posts with the highest number of likes."""
    results = queries.get_top_liked_posts(db)
    return [{"title": r[0], "likes": r[1]} for r in results]

@router.get("/active-users")
def active_users(db: Session = Depends(get_db)):
    """Get users who published the most posts."""
    results = queries.get_most_active_users(db)
    return [{"user": r[0], "posts": r[1]} for r in results]

@router.get("/popular-groups")
def popular_groups(db: Session = Depends(get_db)):
    """List groups ordered by their member count."""
    results = queries.get_popular_groups(db)
    return [{"group": r[0], "members": r[1]} for r in results]

@router.get("/silent-users")
def silent_users(db: Session = Depends(get_db)):
    """List users who have not created any post yet."""
    results = queries.get_silent_users(db)
    return [r[0] for r in results]

@router.get("/avg-comments")
def avg_comments(db: Session = Depends(get_db)):
    """Calculate the average number of comments per post."""
    result = queries.get_avg_comments_per_post(db)
    return {"average_comments": result if result else 0}