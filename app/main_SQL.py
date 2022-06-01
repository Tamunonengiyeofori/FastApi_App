from fastapi import FastAPI,  status, HTTPException, Response
# from fastapi.params import Body
from pydantic import BaseModel 
from typing import Optional
# from fastapi.responses import  
from random import randint
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time 
load_dotenv()

app = FastAPI()

#Create 
class Post(BaseModel):
    title: str
    content: str 
    published: bool = True # The user can decide to publish a post or not so we give it a default value of true  
    rating: Optional[int] = None # The user can choose to add a rating to a post so it's made optional so  if the user doesn't include it, it has no default value instead it defaults to 'None'
  
postgres_pswd = os.getenv("POSTGRESS_PASWD")

#setup postgresql connection and cursor with postgresql DB using the psycopg module
#Loop the connection as long as there is an error so the program only proceeds to setup the fastapi server if there is a database connection

while True:
    try:
        connection = psycopg2.connect(host="localhost" , 
                                    database="fastapi_1" , 
                                    user="postgres" , 
                                    password=postgres_pswd ,
                                    cursor_factory=RealDictCursor) 
        
        cursor = connection.cursor() # save connection in a variable
        print("Successfully Connected to database!!")
        break
        
    except Exception as error:
        print("Connection to Database failed")
        print(f"Error: {error}")
        time.sleep(3) # slow down the time between each reconnection trial by 3 seconds using sleep module
    
my_posts = [
    {
        "title": "title of post 1" , 
        "content": "content of post 1" , 
        "id": 1
    } ,
    { "title": "favourite foods" , 
     "content": "i like afang soup",
     "id": 2
        
    }]

@app.get("/")
def root():
    return{"message":"Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall() 
    return {"data" : posts}

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """ , (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    return{"post_detail" : post}  

@app.post("/posts", status_code=status.HTTP_201_CREATED)    
# def create_post(payload: dict = Body (...)): #Retrieving json content/data from a POST htttp request 
def create_post(post: Post): #Reference the Schema 'Post' class created from the pydantic module and save it in a variable
    # print(payload)
    # return {"post": f"title {payload['title']} content: {payload['content']}"}
    cursor.execute("""INSERT INTO posts (title , content, published) VALUES (%s, %s, %s) RETURNING * 
                   """,
                    (post.title , post.content , post.published)) 
    new_post = cursor.fetchone()
    connection.commit() # this saves the newly created data to the portgresql database
    return{"data" : new_post}
    

# Create a path operator to delete a post
def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i
          
@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""" , (str(id),))
    deleted_post = cursor.fetchone()
    connection.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"The post with id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
        
    
# Create a path operator to update a post
@app.put("/posts/{id}")  
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title =  %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published , (str(id),))) 
    updated_post = cursor.fetchone()
    connection.commit()
    if updated_post == None: # to show error when there is no post index because all the posts have been deleted and the posts list is empty
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , 
                            detail=f"The post with id: {id} does not exist")
    
    return{"data" : updated_post}
    