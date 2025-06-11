
from fastapi import HTTPException, Depends, APIRouter
from typing import List
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.routers import Oauth2

router = APIRouter(
    prefix= "/users",
    tags = ["users"]
)

@router.get("/", response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db), current_user: models.User =
                Depends(Oauth2.get_current_user)):
    users = db.query(models.User).all()
    return users

@router.post("/", response_model = schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=List[schemas.UserOut])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user == None:
        raise HTTPException(
            status_code = 404,
            detail = f"User with id {id} was not found")

    return user


