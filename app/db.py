# import os
# from dotenv import load_dotenv
# # from sqlalchemy.orm import Session
# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

    
# load_dotenv()
# DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
# engine = create_engine(DB_URL)
# Session = sessionmaker()

# Base = declarative_base()
# # class Base(DeclarativeBase):
# #     pass

# Base.metadata.create_all(engine)
# print("Database and tables created successfully.")


##############################################################################################################################################

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# המנוע שמבצע את הפעולות בפועל
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# מחלקה לייצור Sessions (צינורות תקשורת)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# מחלקת הבסיס שממנה ירשו כל המודלים שלנו
Base = declarative_base()

# Dependency - פונקציה שתפתח ותסגור את החיבור בכל בקשת API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()