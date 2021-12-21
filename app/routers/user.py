from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm.session import Session

from ..database import get_db
from .. import models, schemas, utils, oauth2

# Creating a Router 
router = APIRouter(
    prefix='/api/v1/users',
    tags=['user']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
#def create_user(user: schemas.UserCreate, db:Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
def create_user(user: schemas.UserCreate, db:Session = Depends(get_db) ):

    # Creating the Hashing Password 
    hashed_password = utils.hash(user.password)
    # Assign the Hashed Password to the User Object 
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id:int, db:Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == id).first()
    print(db_user)
    if  db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with Id - {id} Not Found")
    return db_user
