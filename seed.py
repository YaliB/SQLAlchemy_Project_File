from sqlalchemy.orm import Session
from app.db import SessionLocal, engine, Base
from app import db_models

def seed_data():
    db = SessionLocal()
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # 1. Seed Users
    if db.query(db_models.User).count() == 0:
        print("Seeding Users...")
        users = [
            db_models.User(name="Alice Johnson", email="alice@example.com", password="password123"),
            db_models.User(name="Bob Smith", email="bob@example.com", password="password123"),
            db_models.User(name="Charlie Brown", email="charlie@example.com", password="password123"),
            db_models.User(name="David Wilson", email="david@example.com", password="password123"),
            db_models.User(name="Eve Adams", email="eve@example.com", password="password123")
        ]
        db.add_all(users)
        db.commit()

    # 2. Seed Groups
    if db.query(db_models.Group).count() == 0:
        print("Seeding Groups...")
        groups = [
            db_models.Group(name="Python Developers", description="A group for Python enthusiasts"),
            db_models.Group(name="FastAPI Fans", description="Discussion about FastAPI framework"),
            db_models.Group(name="SQLAlchemy Experts", description="Deep dive into ORM and SQL")
        ]
        db.add_all(groups)
        db.commit()

    # 3. Seed Posts
    if db.query(db_models.Post).count() == 0:
        print("Seeding Posts...")
        all_users = db.query(db_models.User).all()
        posts = [
            db_models.Post(title="My First Post", content="Hello world!", user_id=all_users[0].id),
            db_models.Post(title="FastAPI is Great", content="I love building APIs", user_id=all_users[0].id),
            db_models.Post(title="SQLAlchemy Tips", content="Use relationships wisely", user_id=all_users[1].id),
            db_models.Post(title="Postgres vs SQLite", content="Postgres is more powerful", user_id=all_users[2].id),
            db_models.Post(title="Learning ORM", content="ORM makes life easier", user_id=all_users[3].id)
        ]
        db.add_all(posts)
        db.commit()

    # 4. Seed Likes (To support business questions like "Top Posts")
    if db.query(db_models.Like).count() == 0:
        print("Seeding Likes...")
        all_posts = db.query(db_models.Post).all()
        likes = [
            db_models.Like(user_id=all_users[1].id, post_id=all_posts[0].id),
            db_models.Like(user_id=all_users[2].id, post_id=all_posts[0].id),
            db_models.Like(user_id=all_users[0].id, post_id=all_posts[2].id),
            db_models.Like(user_id=all_users[3].id, post_id=all_posts[0].id)
        ]
        db.add_all(likes)
        db.commit()

    # 5. Seed Group Memberships (N:M relationship)
    if db.query(db_models.GroupMembership).count() == 0:
        print("Seeding Memberships...")
        all_groups = db.query(db_models.Group).all()
        memberships = [
            db_models.GroupMembership(user_id=all_users[0].id, group_id=all_groups[0].id),
            db_models.GroupMembership(user_id=all_users[1].id, group_id=all_groups[0].id),
            db_models.GroupMembership(user_id=all_users[2].id, group_id=all_groups[1].id)
        ]
        db.add_all(memberships)
        db.commit()

    print("Database Seeded Successfully!")
    db.close()

if __name__ == "__main__":
    seed_data()