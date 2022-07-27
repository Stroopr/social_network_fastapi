from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Response, status, HTTPException, Depends

router = APIRouter(
    prefix="/users",
    tags=["Users"]
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password
    user.password = utils.pwd_hasher(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # retrieve the newly created row in the database with the auto created values
    return new_user


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.UserGetResponse])
def get_user(response: Response, db: Session = Depends(get_db)):

    user = db.query(models.User).all()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"No user found")
    return user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserGetResponse)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"user with id: {id} was not found")
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    query_user_to_delete = db.query(models.User).filter(models.User.id == id)

    user_to_delete = query_user_to_delete.first()

    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exit.")

    if user_to_delete.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"User with id: {id} cannot be deleted by {current_user.username}.")

    query_user_to_delete.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)