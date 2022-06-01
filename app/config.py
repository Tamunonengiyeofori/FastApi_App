from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # Tell pydantic to import environmental variables from the .env file
    class Config:
        env_file = ".env"   
    
settings = Settings() 

#create model with pydantic