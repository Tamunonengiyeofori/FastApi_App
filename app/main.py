from fastapi import FastAPI
from . import models
from .database import engine
#the path operations for post and user from routers.py
from .routers import post, user, auth, vote
from .config import settings
# import CORS from fastapi to handle CORS policy
from fastapi.middleware.cors import CORSMiddleware

# create all the models/tables using sqlalchemy
# models.Base.metadata.create_all(bind=engine)
#This line of code is not needed any more as we are using Alembic to create the tables

app = FastAPI()

origins = ["*"]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ADD the path operations from routers.py to the FastAPI app instance so it will reference them and import them.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


#PATH OPERATIONS  
@app.get("/")
def root():
    return{"message":"Hello World"}

  
