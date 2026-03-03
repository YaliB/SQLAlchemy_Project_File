from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    # Pass the function 'datetime.now' without parentheses to call it per record
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    posts = relationship('Post', back_populates='author', cascade="all, delete-orphan")
    comments = relationship('Comment', back_populates='author', cascade="all, delete-orphan")
    likes = relationship('Like', back_populates='user', cascade="all, delete-orphan")
    
    # Relationships for friendships (sent and received)
    friends_requested = relationship('Friendship', foreign_keys='Friendship.user_id', back_populates='requester', cascade="all, delete-orphan")
    friends_received = relationship('Friendship', foreign_keys='Friendship.friend_id', back_populates='receiver', cascade="all, delete-orphan")
    
    # Relationships for messages
    messages_sent = relationship('Message', foreign_keys='Message.sender_id', back_populates='sender', cascade="all, delete-orphan")
    messages_received = relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver', cascade="all, delete-orphan")
    
    # Groups the user belongs to
    group_memberships = relationship('GroupMembership', back_populates='user', cascade="all, delete-orphan")

    # uselist=False confirms it's a 1-to-1 relationship on the SQLAlchemy side
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Combined logic: unique=True ensures 1-to-1, ondelete="CASCADE" handles cleanup
    user_id = Column(Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        unique=True, nullable=False)

    display_name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    
    # Relationship back to the User model
    user = relationship("User", back_populates="profile")

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post', cascade="all, delete-orphan")
    likes = relationship('Like', back_populates='post', cascade="all, delete-orphan")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    post = relationship('Post', back_populates='comments')
    author = relationship('User', back_populates='comments')

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    post = relationship('Post', back_populates='likes')
    user = relationship('User', back_populates='likes')
    
class Friendship(Base):
    __tablename__ = 'friendships'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    friend_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships with explicit foreign keys
    requester = relationship('User', foreign_keys=[user_id], back_populates='friends_requested')
    receiver = relationship('User', foreign_keys=[friend_id], back_populates='friends_received')
    
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships with explicit foreign keys
    sender = relationship('User', foreign_keys=[sender_id], back_populates='messages_sent')
    receiver = relationship('User', foreign_keys=[receiver_id], back_populates='messages_received')
    
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationship to members through the membership table
    members = relationship('GroupMembership', back_populates='group', cascade="all, delete-orphan")
    
class GroupMembership(Base):
    __tablename__ = 'group_memberships'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id', ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    group = relationship('Group', back_populates='members')
    user = relationship('User', back_populates='group_memberships')