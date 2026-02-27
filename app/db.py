import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from contextlib import contextmanager


load_dotenv() # Load variables from .env file

# Get database URL from environment or default to SQLite
# Format: postgresql://user:password@localhost:5432/db_name
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")

# Only use check_same_thread for SQLite
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Context manager for DB session
@contextmanager
def db_session():
    """
    Context manager for database sessions.
    - Commits on success.
    - Rollbacks on error.
    - Always closes the session.
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()  # Save changes if no exception occurred
    except Exception as e:
        session.rollback() # Undo changes if something went wrong
        raise e
    finally:
        session.close()    # Always release the connection