from .. import models, schemas, utils
from fastapi import FastAPI,  status, HTTPException, Response, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models

#create a router object from the APIRouter class
router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)

# Create a path operation for creating a User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)):
    user_email = db.query(models.User).filter(models.User.email == user.email).first()
    
    if user_email is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                           detail=f"User with username {user_email.email} already exists" )
    # hash user password (user.password)
    user_password = utils.hash(user.password)
    #update user password 
    user.password = user_password
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Create a path operation for getting a User by id
@router.get("/{id}", response_model=schemas.UserOut)
def get_(id: int , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"user with id: {id} does not exist")
    return user  
