# FastAPI CRUD API with PostgreSQL

This project is a RESTful API built with [FastAPI](https://fastapi.tiangolo.com/) that supports full CRUD (Create, Read, Update, Delete) operations on blog posts using both **raw SQL with psycopg2** and **SQLAlchemy ORM**. It connects to a PostgreSQL database and is designed for learning, experimentation, and extensibility.

## 🚀 Features

- FastAPI backend
- PostgreSQL integration
- Raw SQL queries using `psycopg2`
- SQLAlchemy models and ORM setup
- Pydantic schema validation
- Basic exception handling
- Auto-reloading with `uvicorn`

## 🗂️ Project Structure

```
Fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py           # Entry point of the FastAPI app
│   ├── database.py       # PostgreSQL database connection
│   └── models.py         # SQLAlchemy models
```

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

- `GET /posts` - List all posts
- `POST /posts` - Create a new post
- `GET /posts/{id}` - Retrieve a post by ID
- `PUT /posts/{id}` - Update a post
- `DELETE /posts/{id}` - Delete a post
- `GET /sqlalchemy` - Test SQLAlchemy connection

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
