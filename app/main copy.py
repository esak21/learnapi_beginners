from fastapi import FastAPI, Response,status, HTTPException
from fastapi.param_functions import Body
from pydantic import BaseModel
from typing import Optional
from random import randint, randrange

import time
import psycopg2
from  psycopg2.extras import RealDictCursor

app = FastAPI()

# Creating a Pydantic Class for Data Validation 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# Create Connection 
while True:
    try:
        conn = psycopg2.connect(host ='localhost', database = 'learnfastapi', 
        user='postgres', password='esak@123',  cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("INFO: Database Connection was successfull")
        break
    except Exception as error:
        print(f"ERROR: {error}")
        print("ERROR: Connection FAILED")
        time.sleep(5)

# Store Variables temporarily 
my_posts = [
    {"title": "My Initial Post", "content":"My First Content", "id": 1}
]


def find_post(id):
    for post in my_posts:
        if post["id"] == id :
            return post 
def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post['id'] == id:
            return index

@app.get("/")
async def root():
    return {"message": "welcome to fastAPI v2"}

@app.get("/posts")
def posts():
    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()    
    return {"message": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def  create_post(post:Post):
    cursor.execute(""" INSERT INTO posts (title, content, published ) VALUES (%s, %s, %s ) RETURNING * """, (post.title, post.content, post.published))
    new_posts = cursor.fetchone()
    conn.commit()
    return {"data": new_posts}

@app.get('/posts/{id}')
def get_post(id:int):
    cursor.execute(""" SELECT * FROM POSTS WHERE id =  %s """, (str(id), ))
    post = cursor.fetchone()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} is not Found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM POSTS WHERE id = %s RETURNING * """, (str(id), ))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"id {id} doesnot exist")
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute( """ UPDATE POSTS SET TITLE = %s , CONTENT=%s, PUBLISHED=%s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)) )
    post = cursor.fetchone()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} doesnot exists")
    conn.commit()
    return {'data': post}
