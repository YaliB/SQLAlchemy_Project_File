import os
from dotenv import load_dotenv
# from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, declarative_base, sessionmaker

    
load_dotenv()
DB_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URL)
Session = sessionmaker()

Base = declarative_base()
# class Base(DeclarativeBase):
#     pass

Base.metadata.create_all(engine)
print("Database and tables created successfully.")