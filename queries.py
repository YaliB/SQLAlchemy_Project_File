from sqlalchemy import select, func

from db import Session
from models import User

def select_user(session: Session):
    stmt = (
        select(User.id, User.name, func.count(User.id).label("userCount"))
    )
    
    rows = session.execute(stmt).all()