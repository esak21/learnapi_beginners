from typing import ContextManager
from sqlalchemy.orm import relationship

from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP, String
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

class  Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE" ), nullable=False )
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column( TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    owner = relationship("User") # it basically fetch the user based on the user_id 

# Creating the user Model 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


##  Creating a new Table votes 
class Vote(Base):

    __tablename__ = "votes"

    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True) # refering the Posts Table Id Column 
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)

