from fastapi import APIRouter, Response, status, HTTPException, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
    )


@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=schemas.Token)
def login(user_credential: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    # The body post request will be a "Form Data" expecting two field username and password. Not a raw JSON body anymore
    # OAuth2PasswordRequestForm will return a dict with two keys: username and password
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                             detail=f"Email and password don't match")

    if not utils.pwd_verifier(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Email and password don't match")

    access_token = oauth2.create_access_token(data= {"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}