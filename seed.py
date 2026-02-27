from app.db import db_session, engine, Base
from app import db_models
from app.utils.auth_utils import hash_password # Import our hashing utility

def seed_data():
    """
    Seeds the database with initial data, now including hashed passwords.
    """
    print("Starting database seed process...")
    
    Base.metadata.create_all(bind=engine)

    try:
        with db_session() as db:
            # 1. Seed Users with Hashed Passwords
            if db.query(db_models.User).count() == 0:
                print("Seeding Users with hashed passwords...")
                
                # We use the same password for all test users for simplicity
                test_password = hash_password("password123")
                
                users = [
                    db_models.User(name="Alice Johnson", email="alice@example.com", username="alice", password=test_password),
                    db_models.User(name="Bob Smith", email="bob@example.com", username="bob", password=test_password),
                    db_models.User(name="Charlie Brown", email="charlie@example.com", username="charlie", password=test_password),
                    db_models.User(name="David Wilson", email="david@example.com", username="david", password=test_password),
                    db_models.User(name="Eve Adams", email="eve@example.com", username="eve", password=test_password)
                ]
                db.add_all(users)
                db.flush() 

            # 2. Seed Groups
            if db.query(db_models.Group).count() == 0:
                print("Seeding Groups...")
                groups = [
                    db_models.Group(name="Python Developers"),
                    db_models.Group(name="FastAPI Fans"),
                    db_models.Group(name="React Masters")
                ]
                db.add_all(groups)
                db.flush()

            # 3. Seed Posts
            if db.query(db_models.Post).count() == 0:
                print("Seeding Posts...")
                all_users = db.query(db_models.User).all()
                posts = [
                    db_models.Post(title="My First Post", content="Hello world!", user_id=all_users[0].id),
                    db_models.Post(title="FastAPI is Great", content="Building APIs is fun", user_id=all_users[0].id),
                    db_models.Post(title="SQLAlchemy Tips", content="Context managers are awesome", user_id=all_users[1].id),
                    db_models.Post(title="React vs Vue", content="Which one is better?", user_id=all_users[2].id)
                ]
                db.add_all(posts)
                db.flush()

            # 4. Seed Likes
            if db.query(db_models.Like).count() == 0:
                print("Seeding Likes...")
                all_posts = db.query(db_models.Post).all()
                likes = [
                    db_models.Like(user_id=all_users[1].id, post_id=all_posts[0].id),
                    db_models.Like(user_id=all_users[2].id, post_id=all_posts[0].id),
                    db_models.Like(user_id=all_users[3].id, post_id=all_posts[0].id),
                    db_models.Like(user_id=all_users[0].id, post_id=all_posts[2].id)
                ]
                db.add_all(likes)
                
            # 5. Seed Memberships
            if db.query(db_models.GroupMembership).count() == 0:
                print("Seeding Group Memberships...")
                all_groups = db.query(db_models.Group).all()
                memberships = [
                    db_models.GroupMembership(user_id=all_users[0].id, group_id=all_groups[0].id),
                    db_models.GroupMembership(user_id=all_users[1].id, group_id=all_groups[0].id)
                ]
                db.add_all(memberships)

        print("Database Seeded Successfully! All passwords are now hashed.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")

if __name__ == "__main__":
    seed_data()