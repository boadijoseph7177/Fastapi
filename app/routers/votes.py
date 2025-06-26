from fastapi import HTTPException, Depends, APIRouter, status
from typing import List
from app.database import get_db
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.routers import Oauth2

router = APIRouter(
    prefix= "/votes",
    tags = ["votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User =
                Depends(Oauth2.get_current_user)):
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    vote_found = vote_query.first()

    if vote.dir == 1:
        if not vote_found:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {"message": "successfully added vote"}

        else:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already liked post {vote.post_id}.")

    elif vote.dir == 0:
        if vote_found:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "Vote successfully removed"}
        
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist to be removed")


