from db import Session, Base, engine
from models import User, Post

def seed():
    Base.metadata.create_all(engine)
    
    with Session() as session:
        from sqlalchemy import select
        existing = session.execute(select(User)).scalars().first()
        if existing:
            print("Database already seeded. skipping.")
            return

        try:
            user_1 = User(name="Yali", email="yali@gmail.com", password= "YaliPasswordVeryCool1")
            
            session.add_all([user_1])
            session.flush()
            
            post_1 = Post(user_id = user_1.id, title="MyFirstPost", content="OMG")
            session.add_all([post_1])
            
            session.commit()
            print("Database seeded successfuly!")
        except Exception as e:
            session.rollback()
            print("Faild at seeding DB")
            
            
if __name__ == "__main__":
    seed()