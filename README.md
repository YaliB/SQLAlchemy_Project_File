# Social Media API Project
A FastAPI-based social media backend with profile management, posts, analytics, and more.

## 🚀 How to Run the Project
1. Clone the repository
```Bash
git clone <your-repo-url>
cd social-media-api
```
2. Set up a Virtual Environment
```Bash
# Create environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```
3. Install Dependencies
```Bash
pip install -r requirements.txt
```
4. Run the Server
```Bash
uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000.
You can access the interactive documentation (Swagger UI) at http://127.0.0.1:8000/docs.

## 🗄 Database Connection Instructions
The project uses SQLAlchemy as an ORM, allowing flexibility between different database engines.

1. **Configuration:** Connection details are managed in `app/db.py` and can be overridden via an `.env` file.

2. **Default Setup:** By default, the project is configured to use SQLite for easy development. It will automatically create a file named sql_app.db in the root directory upon the first run.

3. **Production (PostgreSQL/MySQL):**

* Create a `.env` file in the root folder.

* Add your connection string: `DATABASE_URL=postgresql://user:password@localhost/dbname`.

4. **Auto-Migrations:** The project uses `Base.metadata.create_all(bind=engine)` in `main.py` to ensure all tables exist on startup.

## 🛠 Menu Structure (Endpoints)
The API is organized into logical routers for easy navigation:

* **Auth:** `/auth/login` - JWT Token generation.

* **Users:** `/users` - Registration, profile updates, and image uploads.

* **Social:** `/posts` - Create/Read/Update/Delete posts.

* `/comments` - Manage comments on posts.

* `/likes` - Like/Unlike functionality.

* `/friendships` - Connect with other users.

* **Messaging & Groups:**

* `/messages` - Private chat history.

* `/groups` & `/group_memberships` - Community management.

* **Analytics:** `/analytics` - Business insights and statistics.

## 📊 Business Questions (Analytics Implementation)
The project implements 5 key business questions to provide insights into user behavior and platform health:

1. **Top 5 Most Liked Posts:** Identify viral content by calculating the sum of likes per post using complex JOINS.
* Endpoint: `GET /analytics/top-posts`

2. **Most Active Users:** Tracks which users are contributing the most content (Posts) to the platform.
* Endpoint: `GET /analytics/active-users`

3. **Group Popularity:** Ranks groups based on their membership count to see which communities are growing fastest.
* Endpoint: `GET /analytics/popular-groups`

4. **Silent Users:** Identifies users who have registered but haven't posted yet (useful for marketing re-engagement).
* Endpoint: `GET /analytics/silent-users`

5. **User Profile Completeness:** (Example) Provides statistics on how many users have uploaded profile pictures or updated their bios.
* Endpoint: `GET /analytics/profile-stats`

📂 File Structure
Plaintext
app/
├── main.py          # Entry point
├── db_models.py     # SQLAlchemy models
├── api_models.py    # Pydantic schemas
├── routers/         # Route handlers
└── crud/            # Database logic