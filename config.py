from pydantic import BaseModel
from functools import lru_cache

import os

from common.db_type import DataBaseType
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME")
    app_port: int = int(os.getenv("APP_PORT"))
    app_host: int = os.getenv("APP_HOST")
    db_type: DataBaseType = DataBaseType.MYSQL
    db_driver: str = os.getenv('DB_DRIVER')
    db_user: str = os.getenv("DB_USER")
    db_password: str = os.getenv("DB_PASSWORD")
    db_host: str = os.getenv("DB_HOST")
    db_name: str = os.getenv("DB_NAME")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
