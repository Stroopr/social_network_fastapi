from sqlalchemy import func
from .. import models, schemas,  oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from fastapi import APIRouter, Response, status, HTTPException, Depends

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.PostVoteResponse])
def get_posts(db: Session = Depends(get_db),
              limit: int = None,
              skip: int = 0,
              search: Optional[str] = ""):

    posts = db.query(models.Post)

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostVoteResponse)
def get_post(id: int, response: Response, db: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    # retrieve the newly created row in the database with the auto created values
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    query_post_to_delete = db.query(models.Post).filter(models.Post.id == id)

    post_to_delete = query_post_to_delete.first()

    if post_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exit.")

    if post_to_delete.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Post with id: {id} cannot be deleted by {current_user.username}.")

    query_post_to_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    query_post_to_update = db.query(models.Post).filter(models.Post.id == id)

    if query_post_to_update.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exit.")

    if query_post_to_update.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Post with id: {id} cannot be updated by {current_user.username}.")

    query_post_to_update.update(post.dict(), synchronize_session=False)
    db.commit()
    return query_post_to_update.first()
