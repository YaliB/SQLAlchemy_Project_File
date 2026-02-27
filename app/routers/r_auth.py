from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..db import get_db # Assuming you have this dependency
from ..utils.auth_utils import verify_password, create_access_token
from .. import db_models

router = APIRouter(tags=['Authentication'])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # 1. Find user
    user = db.query(db_models.User).filter(db_models.User.username == form_data.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # 2. Check password (using our utility)
    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # 3. Create Token
    access_token = create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}