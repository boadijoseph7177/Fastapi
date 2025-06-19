
from fastapi import HTTPException, Depends, APIRouter, status
from typing import List, Optional
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas
from app.routers import Oauth2

router = APIRouter(
    prefix = "/posts",
    tags =  ["posts"]
)


@router.get("/", response_model=List[schemas.ResponsePost])
def get_posts( db: Session = Depends(get_db), current_user: models.User =
                Depends(Oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.post("/", response_model=schemas.ResponsePost)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User =
                Depends(Oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}" , response_model=schemas.ResponsePost )
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User =
                Depends(Oauth2.get_current_user)):
   
    post = db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(
            status_code= 404,
            detail = f"The post with id={id} was not found."
        )
    return post


@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User =
                Depends(Oauth2.get_current_user)):
  
    post = db.query(models.Post).filter(models.Post.id==id)

    if post.first() == None:
        raise HTTPException(
            status_code=404, 
            detail=f"The post with id={id} was not found."
        )
    
    if current_user.id != post.first().owner_id:
        raise HTTPException ( status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthorized to perform this action.")
    
    post.delete(synchronize_session=False)
    db.commit()
   


@router.put("/{id}" , response_model=schemas.ResponsePost)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User =
                Depends(Oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code = 404,
            detail=f"The post with id={id} was not found."
        )
    
    if current_user.id != post.first().owner_id:
        raise HTTPException ( status_code=status.HTTP_403_FORBIDDEN, detail=f"Unauthorized to perform this action.")
    
    
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return post_query.first()