from fastapi import FastAPI,  status, HTTPException, Response, Depends, APIRouter
from typing import List, Optional

from app import Oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, Oauth2
from sqlalchemy import func

#create a router object from the APIRouter class
router = APIRouter(
    prefix="/posts",
    tags = ["Posts"]
)  

#Create a path operation for getting all posts
# @router.get("/", response_model=List[schemas.Post])# Added the List class to return posts as list and avoid an error
@router.get("/", response_model=List[schemas.PostJoinVotesOut], description="")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # print(limit)
    # # add check to make sure a user can only get all posts it created 
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
             models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

#Create a path operation for getting a post by id
@router.get("/{id}", response_model=schemas.PostJoinVotesOut )
def get_post(id: int , db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
         models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    # # add check to make sure a user can only get a post it created by id
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , 
    #                         detail="Not authorized to perform requested action")
    return post  

#Create a path operation for creating a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)     
def create_post(post: schemas.PostCreate , db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    print(current_user.id)   
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
    
#Create a path operator to delete a post
@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int , db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    deleted_post = post_query.first()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"The post with id: {id} was not found")
    
    # add check to make sure a user can only delete a post it created
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , 
                            detail="Not authorized to perform requested action")
        
    post_query.delete(synchronize_session=False)
    #Save the changes to the database
    db.commit()
    # Return a HTTP code is the post is deleted successfully
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
# Create a path operator to update a post
@router.put("/{id}", response_model=schemas.Post)  
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(Oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None: # to show error when there is no post index because all the posts have been deleted and the posts list is empty
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"The post with id: {id} does not exist")
        
    # add check to make sure a user can only update a post it created
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , 
                            detail="Not authorized to perform requested action")
        
    post_query.update(updated_post.dict() , synchronize_session=False)
    #save changes to database
    db.commit()
    return post_query.first()