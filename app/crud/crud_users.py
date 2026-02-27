from sqlalchemy.orm import Session
from ..db_models import User
from ..api_models import UserCreate, UserBase, UserResponse
from ..utils.auth_utils import hash_password # Import our hashing utility

# Get a single user by their ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

# Get a single user by their email (useful for unique checks)
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Get a single user by their username (useful for unique checks)
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

# Get a list of users with optional limit and offset (Pagination)
def get_users(db: Session, skip: int = 0, limit: int = 100):
    # The limit tells the database: What is the maximum number of rows I want to receive right now.
    # The skip (often called offset in SQL) tells the database: How many rows should I jump over before I start counting?
    return db.query(User).offset(skip).limit(limit).all()

# Create a new user in the database
def create_user(db: Session, user: UserCreate):
    # Hash the password BEFORE saving it to the database
    hashed_pwd = hash_password(user.password)
    
    # Map Pydantic data to SQLAlchemy Model
    db_user = User(
        name=user.name,
        email=user.email,
        username=user.username, # Make sure to include username if you added it to models
        password=hashed_pwd     # Saving the hashed version
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Update an existing user's information
def update_user(db: Session, user_id: int, user_data: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = user_data.name
        db_user.email = user_data.email
        db_user.password = user_data.password
        db.commit()
        db.refresh(db_user)
    return db_user

# Delete a user from the database
def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False