from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Creating a Pydantic Class for Data Validation 


# Define the User Schema Model
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config: 
        orm_mode = True



class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


# Defining the login Schema 

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Defie the token 

class Token(BaseModel):
    Token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None