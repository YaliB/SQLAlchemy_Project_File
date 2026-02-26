from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Allows Pydantic to maintain compatibility with ORM objects

# --- Post Schemas ---
class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    user_id: int

class PostResponse(PostBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Comment Schemas ---
class CommentBase(BaseModel):
    content: str
    post_id: int
    user_id: int

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Like Schemas ---
class LikeCreate(BaseModel):
    post_id: int
    user_id: int

class LikeResponse(LikeCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Friendship Schemas ---
class FriendshipCreate(BaseModel):
    user_id: int
    friend_id: int

class FriendshipResponse(FriendshipCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Message Schemas ---
class MessageBase(BaseModel):
    sender_id: int
    receiver_id: int
    content: str

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Group Schemas ---
class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# --- Group Membership Schemas ---
class GroupMembershipCreate(BaseModel):
    group_id: int
    user_id: int

class GroupMembershipResponse(GroupMembershipCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True