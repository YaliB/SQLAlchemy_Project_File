# Database Schema & Relationships
This document describes the database structure and the relationships between the different entities in the Social Media API.

## 📊 Relationships Overview
The system uses **SQLAlchemy ORM** to manage relationships. All relationships are configured with `ondelete="CASCADE"` at the database level and `cascade="all, delete-orphan"` at the ORM level to ensure data integrity.

1. **One-to-One (1:1)**
* **User <-> UserProfile:** Each user has exactly one profile, and each profile belongs to exactly one user.
    * *Foreign Key:* `user_profiles.user_id` -> `users.id` (Unique).

2. **One-to-Many (1:N)**
* **User -> Posts:** One user can create many posts.
* **User -> Comments:** One user can write many comments.
* **User -> Likes:** One user can perform many likes.
* **Post -> Comments:** One post can have many comments.
* **Post -> Likes:** One post can have many likes.

3. **Many-to-Many (M:N)**
* **User <-> Group:** Managed via the `group_memberships` association table.
    * A user can join many groups.
    * A group can have many users.

4. **Self-Referencing / Complex Relationships**
* **Friendships:** Users connecting to other users.
    * Requester: `friendships.user_id`.
    * Receiver: `friendships.friend_id`.

* **Messages:** Direct communication between two users.
    * Sender: `messages.sender_id`.
    * Receiver: `messages.receiver_id`.


## 📑 Table Definitions
<details>
<summary>Click here to see the table[DB] architecture</summary>

**Users Table** (users)
Main table for account information and authentication.
Column | Type | Constraints
`id` | Integer | Primary Key, Index
`username` | String(50) | Unique, Indexed, Not Null
`email` | String(100) | Unique, Indexed, Not Null
`password` | String(255) | Not Null (Hashed)
`created_at` | DateTime | Default: `now()`
</details>