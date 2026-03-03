import os
from fastapi import APIRouter, Depends, HTTPException, status , File, UploadFile
from sqlalchemy.orm import Session
from typing import List

# Internal imports using relative paths
from ..db import SessionLocal, get_db
# from ..db_models import User, UserProfile
from ..api_models import UserCreate, UserResponse, UserProfileUpdate, UserProfileResponse
from ..crud import crud_users 

router = APIRouter()
UPLOAD_DIR = "static/uploads"

# Create a new user
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # 1. Check if user already exists by email
    existing_email = crud_users.get_user_by_email(db, email=user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Check if username is already taken (Important for Login!)
    existing_username = crud_users.get_user_by_username(db, username=user.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # 3. Create new user 
    # Password hashing is now handled at the CRUD level for security.
    return crud_users.create_user(db=db, user=user)


# Get all users (default first 100 users)
@router.get("/", response_model=List[UserResponse])
def get_all_users(skip: int = 0, limit: int = 100,db: Session = Depends(get_db)):
    """
    Retrieve users with pagination.
    - skip: number of records to skip (default 0)
    - limit: maximum number of records to return (default 100)
    """
    return crud_users.get_users(db, skip=skip, limit=limit)


# Get a specific user
@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_users.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Update a user
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate, db: Session = Depends(get_db)):
    existing_user = crud_users.get_user_by_id(db, user_id=user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # model_dump() returns a dictionary of the model fields and their values.
    return crud_users.update_user(db, user_id=user_id, user_data=updated_user)


# Delete a user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    existing_user = crud_users.get_user_by_id(db, user_id=user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return crud_users.delete_user(db, user_id=user_id)


# -------------------------------------------
#               Profile Actions
# -------------------------------------------
@router.post("/{user_id}/upload-profile-pic")
async def upload_image(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Uploads a profile picture for a specific user and updates the UserProfile table.
    """
    # 1. Check if user exists before processing the file
    user_profile = crud_users.get_user_profile(db, user_id)
    if not user_profile:
        raise HTTPException(status_code=404, detail="User profile not found")

    # 2. Ensure the upload directory exists
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # 3. Create a unique file path
    # TODO: Use a library to generate a unique filename to avoid overwriting
    file_extension = os.path.splitext(file.filename)[1]
    safe_filename = f"user_{user_id}_profile{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, safe_filename)
    
    # 4. Save the actual file to the server's disk
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        # Log the error (e.g., logger.error(e))
        raise HTTPException(status_code=500, detail=f"Could not save file to disk: {str(e)}")
    
    # 5. Update the profile picture path in the database using CRUD logic
    profile_update = UserProfileUpdate(profile_picture_url=file_path)
    updated_profile = crud_users.update_user_profile(db, user_id, profile_update)
    
    if not updated_profile:
        # This is a safety check, already verified the user exists in step 1
        raise HTTPException(status_code=404, detail="Failed to update profile record")
        
    return {
        "info": "Picture updated successfully", 
        "path": file_path,
        "display_name": updated_profile
    }

@router.patch("/{user_id}/profile", response_model=UserProfileResponse)
def update_profile(user_id: int, profile: UserProfileUpdate, db: Session = Depends(get_db)):
    """
    Update the display name or bio of a user.
    """
    updated_profile = crud_users.update_user_profile(db, user_id, profile)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="User profile not found")
    return updated_profile