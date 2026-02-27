from fastapi import APIRouter
from typing import List, Dict, Any
from .. import queries

router = APIRouter()

@router.get("/top-posts", response_model=List[Dict[str, Any]])
def get_top_posts():
    """
    Get the 5 posts with the highest number of likes.
    The session is managed internally by the query function.
    """
    results = queries.get_top_liked_posts()
    return [{"title": r[0], "likes": r[1]} for r in results]

@router.get("/active-users", response_model=List[Dict[str, Any]])
def get_active_users():
    """
    Get users who published the most posts.
    """
    results = queries.get_most_active_users()
    return [{"user": r[0], "posts": r[1]} for r in results]

@router.get("/popular-groups", response_model=List[Dict[str, Any]])
def get_popular_groups():
    """
    List groups ordered by their member count.
    """
    results = queries.get_popular_groups()
    return [{"group": r[0], "members": r[1]} for r in results]

@router.get("/silent-users", response_model=List[str])
def get_silent_users():
    """
    List names of users who have not created any post yet.
    """
    results = queries.get_silent_users()
    return [r[0] for r in results]

@router.get("/avg-comments")
def get_avg_comments():
    """
    Calculate the average number of comments per post across the platform.
    """
    result = queries.get_avg_comments_per_post()
    return {"average_comments": round(float(result), 2) if result else 0}