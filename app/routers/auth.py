
#users email and password
# I will hash password and compare it to the hashed password in the database 
from fastapi import HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import utils, schemas, models

router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login")
def login_user(user_credentials: schemas.LoginUser, db: Session = Depends(get_db)):
    user= db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if user == None: raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")

    return {"detail": "User exists and password checks out"}
