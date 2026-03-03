from app.db import db_session, engine, Base
from app import db_models
from app.utils.auth_utils import hash_password
import random

def seed_data():
    """
    Seeds the database with initial data across all tables.
    """
    print("Starting comprehensive database seed process...")
    
    Base.metadata.create_all(bind=engine)

    try:
        with db_session() as db:
            # 1. Seed Users
            if db.query(db_models.User).count() == 0:
                print("Seeding Users...")
                pw = hash_password("password123")
                users = [
                    db_models.User(username="alice", email="alice@test.com", password=pw),
                    db_models.User(username="bob", email="bob@test.com", password=pw),
                    db_models.User(username="charlie", email="charlie@test.com", password=pw),
                    db_models.User(username="david", email="david@test.com", password=pw),
                    db_models.User(username="eve", email="eve@test.com", password=pw),
                    db_models.User(username="frank", email="frank@test.com", password=pw),
                    db_models.User(username="grace", email="grace@test.com", password=pw)
                ]
                db.add_all(users)
                db.flush()

            all_users = db.query(db_models.User).all()

            # 2. Seed User Profiles (1-to-1)
            if db.query(db_models.UserProfile).count() == 0:
                print("Seeding Profiles...")
                profiles = [
                    db_models.UserProfile(user_id=u.id, display_name=f"{u.username.title()} Person", bio=f"I am {u.username}")
                    for u in all_users
                ]
                db.add_all(profiles)
                db.flush()

            # 3. Seed Groups
            if db.query(db_models.Group).count() == 0:
                print("Seeding Groups...")
                groups = [
                    db_models.Group(name="Devs"),
                    db_models.Group(name="Noobies"),
                    db_models.Group(name="Fitness Junkies"),
                    db_models.Group(name="Gaming Zone"),
                    db_models.Group(name="Yali's Fans")
                ]
                db.add_all(groups)
                db.flush()
            
            all_groups = db.query(db_models.Group).all()

            # 4. Seed Group Memberships
            if db.query(db_models.GroupMembership).count() == 0:
                print("Seeding Memberships...")
                memberships = []
                for u in all_users:
                    # Assign each user to 1-2 random groups
                    chosen_groups = random.sample(all_groups, k=2)
                    for g in chosen_groups:
                        memberships.append(db_models.GroupMembership(user_id=u.id, group_id=g.id))
                db.add_all(memberships)
                db.flush()

            # 5. Seed Friendships
            if db.query(db_models.Friendship).count() == 0:
                print("Seeding Friendships...")
                friends = [
                    db_models.Friendship(user_id=all_users[0].id, friend_id=all_users[1].id),
                    db_models.Friendship(user_id=all_users[1].id, friend_id=all_users[2].id),
                    db_models.Friendship(user_id=all_users[2].id, friend_id=all_users[3].id),
                    db_models.Friendship(user_id=all_users[3].id, friend_id=all_users[4].id),
                    db_models.Friendship(user_id=all_users[4].id, friend_id=all_users[0].id)
                ]
                db.add_all(friends)
                db.flush()

            # 6. Seed Posts
            if db.query(db_models.Post).count() == 0:
                print("Seeding Posts...")
                posts = [
                    db_models.Post(user_id=all_users[0].id, title="Hello World", content="My first update!"),
                    db_models.Post(user_id=all_users[1].id, title="Coding", content="Python is amazing."),
                    db_models.Post(user_id=all_users[2].id, title="Work", content="Busy day at the office."),
                    db_models.Post(user_id=all_users[3].id, title="Gym", content="Leg day was brutal."),
                    db_models.Post(user_id=all_users[4].id, title="Coffee", content="Best espresso in town."),
                    db_models.Post(user_id=all_users[0].id, title="Travel", content="Thinking about Japan.")
                ]
                db.add_all(posts)
                db.flush()

            all_posts = db.query(db_models.Post).all()

            # 7. Seed Comments
            if db.query(db_models.Comment).count() == 0:
                print("Seeding Comments...")
                comments = [
                    db_models.Comment(user_id=all_users[1].id, post_id=all_posts[0].id, content="Nice!"),
                    db_models.Comment(user_id=all_users[2].id, post_id=all_posts[0].id, content="Welcome."),
                    db_models.Comment(user_id=all_users[0].id, post_id=all_posts[1].id, content="True story."),
                    db_models.Comment(user_id=all_users[3].id, post_id=all_posts[2].id, content="Keep it up!"),
                    db_models.Comment(user_id=all_users[4].id, post_id=all_posts[3].id, content="No pain no gain.")
                ]
                db.add_all(comments)

            # 8. Seed Likes
            if db.query(db_models.Like).count() == 0:
                print("Seeding Likes...")
                likes = [
                    db_models.Like(user_id=all_users[i].id, post_id=all_posts[0].id) for i in range(1, 5)
                ] + [
                    db_models.Like(user_id=all_users[0].id, post_id=all_posts[1].id),
                    db_models.Like(user_id=all_users[2].id, post_id=all_posts[1].id)
                ]
                db.add_all(likes)

            # 9. Seed Messages
            if db.query(db_models.Message).count() == 0:
                print("Seeding Messages...")
                messages = [
                    db_models.Message(sender_id=all_users[0].id, receiver_id=all_users[1].id, content="Hey Bob!"),
                    db_models.Message(sender_id=all_users[1].id, receiver_id=all_users[0].id, content="Hi Alice!"),
                    db_models.Message(sender_id=all_users[2].id, receiver_id=all_users[3].id, content="Did you see my post?"),
                    db_models.Message(sender_id=all_users[3].id, receiver_id=all_users[2].id, content="Yes, liked it!"),
                    db_models.Message(sender_id=all_users[4].id, receiver_id=all_users[0].id, content="Meeting at 5?")
                ]
                db.add_all(messages)

        print("Full Database Seeded Successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    seed_data()