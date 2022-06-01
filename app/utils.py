# Library for password hashing and security
from passlib.context import CryptContext

# The default hashing algorithm used is Cryptocontext  
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# create a function to compare the two user password hashes for user login
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password , hashed_password)
 