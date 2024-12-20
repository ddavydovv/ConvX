from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv()


class ServerSettings(BaseModel):
    host: str = os.getenv('FASTAPI_HOST')
    port: int = os.getenv('FASTAPI_PORT')


class AlchemySettings(BaseModel):
    url: str = os.getenv('POSTGRES_URL')
    echo: bool = True,
    echo_pool: bool = True,
    max_overflow: int = 10,
    pool_size: int = 50,
    future: bool = True


class CacheSettings(BaseModel):
    url: str = os.getenv('REDIS_URL')


class RabbitSettings(BaseModel):
    url: str = os.getenv('RABBIT_MQ_URL')


class Settings(BaseSettings):
    server: ServerSettings = ServerSettings()
    alchemy: AlchemySettings = AlchemySettings()
    rabbit: RabbitSettings = RabbitSettings()
    cache: CacheSettings = CacheSettings()


settings = Settings()