from sqlalchemy.orm import Session
from ..db_models import User, UserProfile
from ..api_models import UserCreate, UserProfileUpdate
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
    # 1. Create the user
    db_user = User(
        email=user.email,
        username=user.username,
        password=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user) # Refresh the user from the database to get the ID

    # 2. Create the linked profile automatically
    db_profile = UserProfile(
        user_id=db_user.id,
        display_name=user.display_name if user.display_name else user.username
    )
    db.add(db_profile)
    db.commit()
    
    return db_user

# Update an existing user's information
def update_user(db: Session, user_id: int, user_data: UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.email = user_data.email
        db_user.username = user_data.username
        # Hash password if it's being updated
        db_user.password = hash_password(user_data.password)
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






# ----------------------------------------------------------
#                   User Profile Functions
# ----------------------------------------------------------
def get_user_profile(db: Session, user_id: int):
    """
    Fetch the profile associated with a specific user.
    """
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()

def update_user_profile(db: Session, user_id: int, profile_data: UserProfileUpdate):
    """
    Update profile fields. Only updates fields that are actually provided.
    """
    db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not db_profile:
        return None
    
    # Convert Pydantic model to dict, excluding unset fields
    update_data = profile_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile