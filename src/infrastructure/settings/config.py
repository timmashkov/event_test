from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(BaseSettings):
    # Database settings
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Auth settings
    SECRET: str
    X_API_TOKEN: str
    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int

    @property
    def redis_url(self):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    class Config:
        env_file = ".env"


base_config = BaseConfig()
