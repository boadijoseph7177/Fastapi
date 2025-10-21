# PulseAPI: Social Voting Platform API

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-blue?logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-1.4-blue?logo=sqlalchemy)](https://www.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue?logo=postgresql)](https://www.postgresql.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A high-performance, asynchronous REST API for a social voting platform, similar to a backend for Reddit or Hacker News. Built with FastAPI, PostgreSQL, and SQLAlchemy, this project features secure JWT authentication, a robust voting system, and an optimized, modular design.

## Key Features

* **Secure Authentication:** Full user registration and login system using **JWT tokens** (OAuth2) and secure **bcrypt** password hashing.
* **Full CRUD Functionality:** Complete Create, Read, Update, and Delete operations for both users and posts.
* **Robust Voting System:** Users can upvote (`dir=1`) or remove their vote (`dir=0`) from posts.
* **Vote Integrity:** A **composite primary key** (`user_id`, `post_id`) at the database level prevents duplicate votes and race conditions.
* **Ownership Authorization:** Users can only update or delete their *own* posts. Attempts to modify other users' content are rejected with a **403 Forbidden** error.
* **Optimized Vote Counts:** Efficiently calculates and returns the total vote count for posts by using a **SQLAlchemy `JOIN`** with `func.count()`, avoiding the N+1 query problem.
* **Data Validation:** Leverages **Pydantic** schemas for automatic request validation and to ensure API responses never leak sensitive data (like password hashes).
* **Modular Design:** Code is cleanly separated into routers for `auth`, `users`,`posts`, and `votes`, making the project scalable and easy to maintain.

## Tech Stack

* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Database:** [PostgreSQL](https://www.postgresql.org/)
* **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/)
* **Authentication:** [JWT (OAuth2)](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/), [passlib](https://passlib.readthedocs.io/en/stable/)
* **Data Validation:** [Pydantic](https://docs.pydantic.dev/latest/)
* **DB Migrations:** [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* **Server:** [Uvicorn](https://www.uvicorn.org/)

## Project Architecture

The application is built around a clean, modular design centered on separation of concerns.

* `main.py`: The main application entrypoint. Initializes the FastAPI app, mounts CORS middleware, and includes the routers.
* `database.py`: Manages the PostgreSQL database connection (`engine`) and provides a reusable dependency (`get_db`) for managing `SessionLocal`.
* `models.py`: Defines the database tables (`User`, `Post`, `Vote`) using SQLAlchemy's declarative `Base`.
* `schemas.py`: Defines the Pydantic models used for API data validation (e.g., `PostCreate`, `UserCreate`) and response shaping (e.g., `PostOut`, `UserOut`).
* `routers/`: A directory containing the app's API logic, split by concern:
    * `auth.py`: Handles the `/login` endpoint for token generation.
    * `users.py`: Handles user registration and retrieval.
    * `posts.py`: Handles all CRUD operations for posts, protected by the `get_current_user` dependency.
    * `votes.py`: Handles the logic for casting and removing votes.
* `Oauth2.py`: Contains all security-related utility functions for creating, verifying, and decoding JWTs, including the core `get_current_user` dependency.
* `config.py`: Loads environment variables (like database credentials and JWT secrets) using Pydantic's `BaseSettings`.

## Getting Started

### Prerequisites

* Python 3.9+
* PostgreSQL Server

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/boadijoseph7177/Fastapi.git](https://github.com/boadijoseph7177/Fastapi.git)
    cd Fastapi
    ```

2.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

3.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your database credentials and a JWT secret.

    ```.env
    DATABASE_HOSTNAME=localhost
    DATABASE_PORT=5432
    DATABASE_PASSWORD=your_db_password
    DATABASE_NAME=your_db_name
    DATABASE_USERNAME=postgres
    SECRET_KEY=your_super_secret_jwt_key
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

4.  **Run database migrations:**
    (This project is set up with Alembic for database migrations.)
    ```sh
    alembic upgrade head
    ```

5.  **Run the application:**
    ```sh
    uvicorn app.main:app --reload
    ```
    The API will be available at `http://localhost:8000` and the automatic documentation at `http://localhost:8000/docs`.

## API Endpoints

### Authentication

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/login` | Authenticates a user and returns a JWT access token. |

### Users

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/users` | Registers a new user. |
| `GET` | `/users` | (Auth) Gets a list of all users. |
| `GET` | `/users/{id}` | Gets details for a specific user. |

### Posts

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/posts` | (Auth) Gets a list of all posts with vote counts. |
| `POST` | `/posts` | (Auth) Creates a new post. |
| `GET` | `/posts/{id}` | (Auth) Gets a single post with its vote count. |
| `PUT` | `/posts/{id}` | (Auth) Updates a post. (Requires ownership) |
| `DELETE` | `/posts/{id}` | (Auth) Deletes a post. (Requires ownership) |

### Votes

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/votes` | (Auth) Casts or removes a vote on a post. |
