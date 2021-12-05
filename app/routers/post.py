from fastapi import status, Depends, HTTPException, Response, APIRouter
from sqlalchemy.orm.session import Session
from typing import List, Optional
import time
import psycopg2
from  psycopg2.extras import RealDictCursor
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy import func
from ..database import get_db
from .. import models, schemas, utils, oauth2

router = APIRouter(
    prefix='/api/v1/posts', 
    tags= ['post']
)


#@router.get('/', response_model=List[schemas.PostResponse])
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db), limit:int = 10, skip:int = 0, search:Optional[str] = "" ):
    # Query Parameter
    print(limit)
    # lets Access the databse Object 
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # By default it will be left Inner Join 
    # 
    results = db.query(models.Post.id, models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    return  results

@router.get('/myposts', response_model=List[schemas.PostResponse])
def get_posts(db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    # lets Access the databse Object 
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.id ).all()    
    return  posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate , db:Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.email)
    print(current_user.id)
    # lets Access the databse Object 
    #new_posts = models.Post(title= post.title, content=post.content, published=post.published)
    new_posts = models.Post(user_id =current_user.id , **post.dict())
    # lets add this Post to Database 
    db.add(new_posts)
    # Lets Commit the changes 
    db.commit()
    # Lets Return the Updated data 
    db.refresh(new_posts)

    return  new_posts



@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db:Session = Depends(get_db)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post.id, models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="POst ID {id} is not created")
    return post

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, post: schemas.PostCreate, db:Session = Depends(get_db), user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id )
    dbpost = post_query.first()
    print(post)

    if dbpost is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "POST ID {id} is not Found")
    
    if dbpost.user_id != user.id :
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="NOT AUTHORISED TO PERFORM DELETE THE POST")
    
    post_query.update(post.dict(), synchronize_session=False)
    #new_posts = models.Post(**post.dict())
    
    db.commit()
    
    return  post_query.first()


@router.delete("/{id}")
def delete_post(id:int, db:Session = Depends(get_db), user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter( models.Post.id == id )
    # Above Db.query() will return a query Object 
    # inorder to convert it to POst Object we have to use the first() method 
    post = post_query.first()
    if post is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "POST ID {id} is not FOUND ")
    if post.user_id != user.id :
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="NOT AUTHORISED TO PERFORM DELETE THE POST")
    # delete the REcords 
    post.delete(synchronize_session=False)
    db.commit()
    
    return {"data": "deleted"}

