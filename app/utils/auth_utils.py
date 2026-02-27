from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

# Setup password hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key to sign JWT tokens (Keep this secret!)
SECRET_KEY = os.getenv("SECRET_KEY_PASSWORDS_HASHING", "!@$%&*()_+~")
ALGORITHM = "HS256"

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)