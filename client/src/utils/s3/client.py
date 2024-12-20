import io
from contextlib import asynccontextmanager

from aiobotocore.session import get_session

from client.src.config import settings


class S3Client:

    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str
    ):
        self.config = {
            'aws_access_key_id': access_key,
            'aws_secret_access_key': secret_key,
            'endpoint_url': endpoint_url
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client('s3', **self.config) as client:
            yield client

    async def upload_file(self, filename: str, file_stream: io.BytesIO):
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file_stream
            )

    async def download_file(self, filename: str) -> io.BytesIO:
        async with self.get_client() as client:
            response = await client.get_object(Bucket=self.bucket_name, Key=filename)
            file_stream = io.BytesIO(await response['Body'].read())
            return file_stream


s3_client = S3Client(
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    endpoint_url=settings.s3.endpoint_url,
    bucket_name=settings.s3.bucket_name
)