from pydantic_settings import BaseSettings
from pydantic import BaseModel
from dotenv import load_dotenv
import os


load_dotenv()


class CacheSettings(BaseModel):
    url: str = os.getenv('REDIS_URL')


class S3Settings(BaseModel):
    access_key: str = os.getenv('S3_ACCESS_KEY')
    secret_key: str = os.getenv('S3_SECRET_KEY')
    endpoint_url: str = os.getenv('S3_ENDPOINT_URL')
    bucket_name: str = os.getenv('S3_BUCKET_NAME')


class RabbitSettings(BaseModel):
    url: str = os.getenv('RABBIT_MQ_URL')


class BotSettings(BaseModel):
    bot_token: str = os.getenv('BOT_TOKEN')


class Settings(BaseSettings):
    cache: CacheSettings = CacheSettings()
    s3: S3Settings = S3Settings()
    rabbit: RabbitSettings = RabbitSettings()
    bot: BotSettings = BotSettings()


settings = Settings()