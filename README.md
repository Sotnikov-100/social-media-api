# Social Media API

A REST API for a social media platform built with Django REST Framework.

---

## Features

- User registration and JWT authentication
- User profile management
- Follow and unfollow other users
- Create, read, update, delete posts
- Like and comment on posts
- Feed with posts from followed users
- Scheduled post creation using Celery
- Hashtag support
- Swagger/ReDoc API documentation

---

## Technologies Used

- Django & Django REST Framework
- PostgreSQL
- Docker & Docker Compose
- Celery + Redis (for asynchronous tasks)
- JWT Authentication

---

## 🚀 How to run locally?

1. **Clone the repository**:
   ```bash
   git@github.com:Sotnikov-100/social-media-api.git && cd social-media-api
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   ```

3. **Start containers**:
   ```bash
   docker-compose up --build -d
   ```

--- 

## API Endpoints Overview

🔐**Authentication**

| Method | Endpoint              | Description                      |
| ------ | --------------------- | -------------------------------- |
| POST   | `/api/token/`         | Obtain access and refresh tokens |
| POST   | `/api/token/refresh/` | Refresh access token             |


👤**Users & Profiles**

| Method | Endpoint                        | Description                   |
| ------ | ------------------------------- | ----------------------------- |
| GET    | `/api/users/{id}/`              | Get another user's profile    |
| GET    | `/api/users/profile/`           | Get your own profile          |
| PUT    | `/api/users/profile/`           | Update your profile           |
| PATCH  | `/api/users/profile/`           | Partially update your profile |
| POST   | `/api/users/register/`          | Register a new user           |
| GET    | `/api/users/search/?search=...` | Search for users              |


📌**Following**

| Method | Endpoint                         | Description                       |
| ------ | -------------------------------- | --------------------------------- |
| GET    | `/api/follows/followers/`        | Retrieve list of followers        |
| GET    | `/api/follows/following/`        | Retrieve list of users you follow |
| POST   | `/api/follows/user/{id}/follow/` | Follow a user by ID               |
| DELETE | `/api/follows/user/{id}/follow/` | Unfollow a user by ID             |


📝**Posts**

| Method | Endpoint                  | Description                  |
| ------ | ------------------------- | ---------------------------- |
| GET    | `/api/posts/`             | List all published posts     |
| GET    | `/api/posts/{id}/`        | Retrieve post details        |
| PUT    | `/api/posts/{id}/`        | Update a post (full update)  |
| PATCH  | `/api/posts/{id}/`        | Partially update a post      |
| DELETE | `/api/posts/{id}/`        | Delete a post                |
| POST   | `/api/posts/create/`      | Create a new post            |
| GET    | `/api/posts/feed/`        | Get feed from followed users |
| GET    | `/api/posts/liked/`       | Get liked posts              |
| GET    | `/api/posts/my/`          | Get your own posts           |
| GET    | `/api/posts/?hashtag=tag` | Search posts by hashtag      |


👍**Likes**

| Method | Endpoint                | Description             |
| ------ | ----------------------- | ----------------------- |
| POST   | `/api/posts/{id}/like/` | Like a post             |
| DELETE | `/api/posts/{id}/like/` | Remove like from a post |

💬 **Comments**

| Method | Endpoint                    | Description                  |
| ------ | --------------------------- | ---------------------------- |
| GET    | `/api/posts/{id}/comments/` | Retrieve comments for a post |
| POST   | `/api/posts/{id}/comments/` | Add a comment to a post      |
| GET    | `/api/posts/comments/{id}/` | Get comment details          |
| PUT    | `/api/posts/comments/{id}/` | Update comment (full)        |
| PATCH  | `/api/posts/comments/{id}/` | Partially update comment     |
| DELETE | `/api/posts/comments/{id}/` | Delete a comment             |
