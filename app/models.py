from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    # Pass the function 'datetime.now' without parentheses to call it per record
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    posts = relationship('Post', back_populates='author')
    comments = relationship('Comment', back_populates='author')
    likes = relationship('Like', back_populates='user')
    
    # Relationships for friendships (sent and received)
    friends_requested = relationship('Friendship', foreign_keys='Friendship.user_id', back_populates='requester')
    friends_received = relationship('Friendship', foreign_keys='Friendship.friend_id', back_populates='receiver')
    
    # Relationships for messages
    messages_sent = relationship('Message', foreign_keys='Message.sender_id', back_populates='sender')
    messages_received = relationship('Message', foreign_keys='Message.receiver_id', back_populates='receiver')
    
    # Groups the user belongs to
    group_memberships = relationship('GroupMembership', back_populates='user')

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    author = relationship('User', back_populates='posts')
    comments = relationship('Comment', back_populates='post')
    likes = relationship('Like', back_populates='post')

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    post = relationship('Post', back_populates='comments')
    author = relationship('User', back_populates='comments')

class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    post = relationship('Post', back_populates='likes')
    user = relationship('User', back_populates='likes')
    
class Friendship(Base):
    __tablename__ = 'friendships'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    friend_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships with explicit foreign keys
    requester = relationship('User', foreign_keys=[user_id], back_populates='friends_requested')
    receiver = relationship('User', foreign_keys=[friend_id], back_populates='friends_received')
    
class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.id'), nullable=False)
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
    members = relationship('GroupMembership', back_populates='group')
    
class GroupMembership(Base):
    __tablename__ = 'group_memberships'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    group = relationship('Group', back_populates='members')
    user = relationship('User', back_populates='group_memberships')