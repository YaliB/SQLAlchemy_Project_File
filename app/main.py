from fastapi import FastAPI
from app.routers import (r_comments, r_friendships, r_group_memberships, r_groups, r_likes, r_messages, r_posts, r_users, r_analytics)
from .db import Base, engine


# Create tables on startup
Base.metadata.create_all(bind=engine)

# Init the FastAPI Server
app = FastAPI(title="Social Media API")

# Include the Routers
app.include_router(r_users.router, prefix="/users", tags=["users"])
app.include_router(r_posts.router, prefix="/posts", tags=["posts"])
app.include_router(r_comments.router, prefix="/comments", tags=["comments"])
app.include_router(r_likes.router, prefix="/likes", tags=["likes"])
app.include_router(r_friendships.router, prefix="/friendships", tags=["friendships"])
app.include_router(r_messages.router, prefix="/messages", tags=["messages"])
app.include_router(r_groups.router, prefix="/groups", tags=["groups"])
app.include_router(r_group_memberships.router, prefix="/group_memberships", tags=["group_memberships"])
app.include_router(r_analytics.router, prefix="/analytics", tags=["analytics"])

# Root Routhe
@app.get("/")
def root():
    return {"message": "Welcome to the Social Media API"}
def main():
    print("Project started successfully!")
          
if __name__ == "__main__":
    main()

