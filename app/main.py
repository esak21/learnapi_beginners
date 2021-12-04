from fastapi import FastAPI
from .database import  engine
from . import models
from .routers import post, user, auth, vote
from .config import settings
# setting up Cors 
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_username)

# Creating the SQLALCHMEY Conenction 
# Since we have the Alembic Now we dont need the below line 
#models.Base.metadata.create_all(bind=engine)

# Creating the FATAPI APP 
app = FastAPI()

# ADDING Middleware 
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://www.google.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ADDING ROUTER ROUTES
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


