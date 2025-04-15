from fastapi import FastAPI, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

data = [{
        "title": "Awesome Florida Beach", 
        "content": "Come have fun in Florida Fellas!!!", 
        "id": 1
        },
        {
        "title": "Awesome Kansas Beach", 
        "content": "Come have fun in Kansas Babies!!!", 
        "id": 2
        }
]


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
    return {"data": data}
    print(data)

    
@app.post("/posts")
def create_post(post: Post):
    post.id = randrange(1, 100000)
    new_post = post.dict()
    data.append(new_post)
    print(new_post)
    return {"data": data}

def get_one_post(id):
    for p in data:
        if p["id"] == id:
            return p
    return None


@app.get("/posts/{id}")
def get_post(id: int):
    post = get_one_post(id)
    if not post:
        raise HTTPException(
            status_code= 404,
            detail = f"The post with id={id} was not found."
        )
    return {"details": post}

def delete_one_post(id):
    for i,post in enumerate(data):
        if post["id"] == id:
            return data.pop(i)
    return None

@app.delete("/posts/{id}")
def delete_post(id: int):
    deleted_post = delete_one_post(id)
    if not deleted_post:
        raise HTTPException(
            status_code=404, 
            detail=f"The post with id={id} was not found."
        )
    return {"detail": f"Post {deleted_post} has been successfully deleted!"}

def get_postid(id):
    for index,p in enumerate(data):
        if p["id"] == id:
            return index
    return None

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = get_postid(id)
    Post_dict = post.dict()
    if index == None:
        raise HTTPException(
            status_code = 404,
            detail=f"The post with id={id} was not found."
        )
    Post_dict["id"] = id
    data[index] = Post_dict
    return f"The post with id {id} has been successfully updated."