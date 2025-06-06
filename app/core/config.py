from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str
    USERS_COLLECTION_NAME: str
    PROFILES_COLLECTION_NAME : str
    FOLLOWERS_COLLECTION_NAME : str
    DB_URL : str
    DB_NAME : str
    ALGORITHM : str
    ACCESS_TOKEN_JWT_SUBJECT : str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES : int

    class Config:
        env_file = ".env"

settings = Settings()