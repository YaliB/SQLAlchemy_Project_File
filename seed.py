from app.db import db_session, engine, Base
from app import db_models

def seed_data():
    """
    Main function to seed the database with initial data.
    Uses the db_session context manager to ensure safe transactions.
    """
    print("Starting database seed process...")
    
    # Ensure all tables exist (works for both SQLite and PostgreSQL)
    Base.metadata.create_all(bind=engine)

    try:
        with db_session() as db:
            # 1. Seed Users
            # Only seed if the table is empty to avoid Unique Constraint errors
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
                db.flush() # Push changes to get IDs for foreign key relations

            # 2. Seed Groups
            if db.query(db_models.Group).count() == 0:
                print("Seeding Groups...")
                groups = [
                    db_models.Group(name="Python Developers", description="A group for Python enthusiasts"),
                    db_models.Group(name="FastAPI Fans", description="Discussion about FastAPI framework"),
                    db_models.Group(name="React Masters", description="Frontend development hub")
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
                    db_models.GroupMembership(user_id=all_users[0].id, group_id=all_groups[0].id, role="admin"),
                    db_models.GroupMembership(user_id=all_users[1].id, group_id=all_groups[0].id, role="member")
                ]
                db.add_all(memberships)

        print("Database Seeded Successfully! All changes committed.")

    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        # The db_session context manager will automatically handle rollback

if __name__ == "__main__":
    seed_data()