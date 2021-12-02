from fastapi import FastAPI
from .database import  engine
from . import models
from .routers import post, user, auth, vote
from .config import settings


print(settings.database_username)

# Creating the SQLALCHMEY Conenction 
models.Base.metadata.create_all(bind=engine)
# Creating the FATAPI APP 
app = FastAPI()

# ADDING ROUTER ROUTES
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


