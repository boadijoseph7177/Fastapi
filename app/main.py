from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models
from app.database import engine,get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    id: Optional[int] = None

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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts")
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #     (post.title, post.content, post.published))

    # new_post = cursor.fetchone()
    # conn.commit()
    # return {"data": new_post}
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(
            status_code= 404,
            detail = f"The post with id={id} was not found."
        )
    return {"details": post}


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
   


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE 
    id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(
            status_code = 404,
            detail=f"The post with id={id} was not found."
        )
    
    return f"The post with id {id} has been successfully updated."