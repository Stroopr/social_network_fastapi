from .. import models, schemas,  oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import APIRouter, Response, status, HTTPException, Depends


router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote: schemas.Vote, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):

    query_post = db.query(models.Post).filter(models.Post.id==vote.post_id)

    post = query_post.first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exit.")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"Vote successfully added"}
    else:
        if found_vote is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Vote successfully deleted"}