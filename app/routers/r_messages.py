from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from ..db import get_db
from .. import api_models
from ..crud import crud_messages

router = APIRouter()

# CREATE - Create a new message
@router.post("/", response_model=api_models.MessageResponse, status_code=status.HTTP_201_CREATED)
def send_private_message(message: api_models.MessageCreate, db: Session = Depends(get_db)):
    # Stores a message between sender and receiver
    return crud_messages.send_message(db, message)

# READ - Get all messages between two users
@router.get("/chat/{user1}/{user2}", response_model=List[api_models.MessageResponse])
def get_chat_history(user1: int, user2: int, db: Session = Depends(get_db)):
    # Fetches conversation history between two users
    return crud_messages.get_conversation(db, user1, user2)