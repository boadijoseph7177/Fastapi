from fastapi import FastAPI, HTTPException, Response, status, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
from typing import Optional, List
import psycopg2

from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import engine,get_db
from app.routers import posts, users, auth



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

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)







