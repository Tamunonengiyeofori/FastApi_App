#PYDANTIC SCHEMA
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime


#Create pydantic schema models

#Post creation and updating model
class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True
    
class PostCreate(PostBase):
    pass

#User Response model
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    #convert sqlalchemy model to pydantic model
    class Config:
        orm_mode = True
    
# Post Response model
class Post(PostBase):
    # This class inherits from the postbase class and also inherits the columns 
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    #convert sqlalchemy model to pydantic model
    class Config:
        orm_mode = True

# Post Response model after joining posts and votes tables
class PostJoinVotesOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True
    
#User creation and updating model
class UserCreate(BaseModel):
    #EmailStr datatype ensures that the user's email is a valid email
    email: EmailStr     
    password: str 
    

#model for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
#model for user JWT token
class Token(BaseModel):
    access_token: str
    token_type: str
    
# model for data embedded in token
class TokenData(BaseModel):
    id: Optional[str] = None
    
# model for vote
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # using conint from pydantic to validate/make-sure that vote dir is 1 or zero
    