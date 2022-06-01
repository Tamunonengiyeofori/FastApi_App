from fastapi import FastAPI,  status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, database, Oauth2

router = APIRouter(
    prefix = "/vote",
    tags = ["Vote"]
)

# create a path operation for creating a vote and voting
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote , db: Session = Depends(database.get_db), current_user: int = Depends(Oauth2.get_current_user)):
    #check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"The post with id: {vote.post_id} does not exist")
    #check if vote already exists(i.e post was already liked by a user)by searching for vote id and current user id of user who created the post.
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                              models.Vote.user_id == current_user.id)
    #Query database to find the vote already liked by user
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already voted on post with id of {vote.post_id}")
        new_vote = models.Vote(user_id = current_user.id,
                            post_id = vote.post_id)
        db.add(new_vote)
        db.commit()
        return{"message": "Successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"vote does not exist")
            
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"Succesfully deleted vote"}