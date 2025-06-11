# FastAPI CRUD API with PostgreSQL

This project is a RESTful API built with [FastAPI](https://fastapi.tiangolo.com/) that supports full CRUD (Create, Read, Update, Delete) operations on blog posts using both **raw SQL with psycopg2** and **SQLAlchemy ORM**. It connects to a PostgreSQL database and is designed for learning, experimentation, and extensibility.

## 🚀 Features

| Category | Details |
|----------|---------|
| **Posts CRUD** | Create, read, update, delete blog posts with raw SQL **and** SQLAlchemy. |
| **User system** | `users` table (`id`, `email`, `password_hash`, `created_at`, `is_active`, `is_superuser`). |
| **Auth** | OAuth2 password flow → time‑bound **JWT** access tokens (`/login`). |
| **Password security** | One‑way hashing with **passlib[bcrypt]**. |
| **Validation** | Strict request/response models via **Pydantic v2**. |
| **Docs** | Automatic OpenAPI at `/docs` (Swagger) and `/redoc`. |
| **Migrations** | **Alembic** keeps the DB schema in sync. |
| **Docker** | `docker compose up` spins up API + Postgres + pgAdmin. |
| **Hot‑reload** | Fast dev loop with **uvicorn --reload**. |

## 🗂️ Project Structure

```
Fastapi/
├── app/
│ ├── main.py # FastAPI instance & router registry
│ ├── core/
│ │ ├── config.py # load settings from .env
│ │ ├── security.py # JWT helpers (create/verify)
│ │ └── deps.py # common dependencies (get_db, get_current_user)
│ ├── database.py # engine, SessionLocal, Base
│ ├── models.py # SQLAlchemy models (User, Post)
│ ├── schemas.py # Pydantic models
│ ├── crud.py # DB helper functions
│ └── routers/
│ ├── auth.py # /users, /login routes
│ └── posts.py # /posts routes
├── alembic/ # migrations
├── tests/ # Pytest suites
├── docker-compose.yml # api, db, pgadmin stack
├── .env.example # sample environment variables
└── README.md

## 📦 Requirements

- Python 3.8+
- PostgreSQL
- pip

Install dependencies:

```bash
pip install -r requirements.txt
```

> If `requirements.txt` doesn’t exist yet, you can generate one with:
> ```bash
> pip freeze > requirements.txt
> ```

## 🛠️ Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/boadijoseph7177/Fastapi.git
cd Fastapi
```

2. **Set up PostgreSQL**

Make sure PostgreSQL is running and create a database named `fastapi`. Update your connection details in `main.py` and `database.py` if needed:

```python
psycopg2.connect(
    host='localhost',
    database='fastapi',
    user='postgres',
    password='yourpassword'
)
```

3. **Run the API**

```bash
uvicorn app.main:app --reload
```

Visit the docs at [http://localhost:8000/docs](http://localhost:8000/docs)

## 🧪 Example Endpoints

| Route         | Method | Auth | Purpose              |
| ------------- | ------ | ---- | -------------------- |
| `/posts`      | GET    | ❌    | List posts           |
| `/posts`      | POST   | ✅    | Create post          |
| `/posts/{id}` | GET    | ❌    | Retrieve post        |
| `/posts/{id}` | PUT    | ✅    | Update own post      |
| `/posts/{id}` | DELETE | ✅    | Delete own post      |
| `/users`      | POST   | ❌    | Register user        |
| `/login`      | POST   | ❌    | Obtain JWT           |
| `/users/me`   | GET    | ✅    | Current user profile |


## 🧰 Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [psycopg2](https://www.psycopg.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Uvicorn](https://www.uvicorn.org/)

## 📌 TODOs

- [ ] Add user authentication
- [ ] Use environment variables for database credentials
- [ ] Create modular route structure
- [ ] Add unit tests

## 📄 License

This project is licensed under the MIT License.

---

Built with ❤️ by [Joseph Boadi](https://github.com/boadijoseph7177)
