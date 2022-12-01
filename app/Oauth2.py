# JWT creation and Oauth2
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #TokenUrl is the endpoint for user login


#SECRET_KEY
#Algorithm for hashing secret key
#Token Expiration time
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
REFRESH_SECRET_KEY = '3617e6110c08550683dda2094022ef654361b5420b7f84c599be8ce57885c79a'

def create_access_token(data: dict):
    to_encode = data.copy() # create a copy of the data dictionary parameter for jwt payload
    expire = datetime.utcnow() + timedelta(minutes = settings.access_token_expire_minutes)
    to_encode.update({"exp": expire}) # update payload with expiry time 
    #Create Jwt token
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm = settings.algorithm)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[settings.algorithm])
        id: str = payload.get("user_id")
        
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)
    
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
