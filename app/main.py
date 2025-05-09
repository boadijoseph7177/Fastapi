from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional, List
import psycopg2
from passlib.context import CryptContext
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine,get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

    
while True:
    try: 
        conn = psycopg2.connect(host = 'localhost', database='fastapi', user='postgres', 
        password='Bjoecr7177', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection was successful!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.ResponsePost])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post("/posts")
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #     (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data": new_post}
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

@app.get("/posts/{id}" , response_model=schemas.ResponsePost)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(
            status_code= 404,
            detail = f"The post with id={id} was not found."
        )
    return post


@app.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise HTTPException(
            status_code=404, 
            detail=f"The post with id={id} was not found."
        )
    post.delete(synchronize_session=False)
    db.commit()
   


@app.put("/posts/{id}" , response_model=schemas.ResponsePost)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE 
    # id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code = 404,
            detail=f"The post with id={id} was not found."
        )
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()


@app.get("/users", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@app.post("/users", response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


