from sqlalchemy.orm import Session
from ..db_models import Message
from .. import api_models

# Create a new message
def send_message(db: Session, message: api_models.MessageCreate):
    db_message = Message(
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

# Fetch messages between two specific users
def get_conversation(db: Session, user_a: int, user_b: int):
    return db.query(Message).filter(
        ((Message.sender_id == user_a) & (Message.receiver_id == user_b)) |
        ((Message.sender_id == user_b) & (Message.receiver_id == user_a))
    ).order_by(Message.created_at).all()