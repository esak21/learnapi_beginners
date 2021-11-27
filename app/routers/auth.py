from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(
    prefix= '/api/v1/auth',
    tags = ['Authentication']
)

@router.post('/login', response_model = schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends() , db:Session = Depends(get_db)):
    # By Default OAuth2PasswordRequestForm store the email in the Field called userName 
    # if the user send email or username or anythin it stores in the username field 
    # it Returns username, password 
    db_user = db.query(models.User).filter(models.User.email == user_credentials.username ).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    # hasing the provided Password 
    if not utils.verifyPassword(user_credentials.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")

    # CReate Token 
    access_token = oauth2.create_access_token(data = {"user_id":db_user.id})

    return {"Token": access_token , "token_type": "bearer"}
    


