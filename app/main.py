from fastapi import FastAPI
from app.routers import (users as users_r,
                        posts as posts_r,
                        comments as comments_r,
                        likes as likes_r,
                        friendships as friendships_r,
                        messages as messages_r,
                        groups as groups_r,
                        group_memberships as GroupMemberships_r)
from .db import Base, engine


# Create tables on startup
Base.metadata.create_all(bind=engine)

# Init the FastAPI Server
app = FastAPI(title="Social Media API")

# Include the Routers
app.include_router(users_r.router, prefix="/users", tags=["users"])
app.include_router(posts_r.router, prefix="/posts", tags=["posts"])
app.include_router(comments_r.router, prefix="/comments", tags=["comments"])
app.include_router(likes_r.router, prefix="/likes", tags=["likes"])
app.include_router(friendships_r.router, prefix="/friendships", tags=["friendships"])
app.include_router(messages_r.router, prefix="/messages", tags=["messages"])
app.include_router(groups_r.router, prefix="/groups", tags=["groups"])
app.include_router(GroupMemberships_r.router, prefix="/group_memberships", tags=["group_memberships"])

# Root Routhe
@app.get("/")
def root():
    return {"message": "Welcome to the Social Media API"}
def main():
    print("Project started successfully!")
          
if __name__ == "__main__":
    main()

