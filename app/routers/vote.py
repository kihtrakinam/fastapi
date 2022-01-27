from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db

router = APIRouter(prefix = "/votes" ,tags = ["Votes"])

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote : schemas.VoteData, db : Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    ## if post not found
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Post id : {vote.post_id} does not exist")

    ## User voting for his own post is forbidden
    else:
        post_user_id = post.user_id
        if post_user_id == current_user.id:
            raise HTTPException(status_code = status.HTTP_403_FORBIDDEN)

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.vote_dir == True:
        if found_vote is None:
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message" : "Successfully added vote"}
        else:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = f"Action already performed by user id : {current_user.id}")   
    else:
        if found_vote is None:
            raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Vote already does not exist")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message" : "Successfully deleted vote"}
            