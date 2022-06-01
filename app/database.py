from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
import os

from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False , autoflush=False, bind=engine)
Base = declarative_base()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# postgres_pswd = os.getenv("POSTGRESS_PASWD")

# while True:
#     try:
#         connection = psycopg2.connect(host="localhost" , 
#                                     database="fastapi_2" , 
#                                     user="postgres" , 
#                                     password=postgres_pswd ,
#                                     cursor_factory=RealDictCursor) 
        
#         cursor = connection.cursor() # save connection in a variable
#         print("Successfully Connected to database!!")
#         break
        
#     except Exception as error:
#         print("Connection to Database failed")
#         print(f"Error: {error}")
#         time.sleep(3) # slow down the time between each reconnection trial by 3 seconds using sleep module
    