import io
import boto3
from botocore.exceptions import NoCredentialsError

from servers.processing.src.config import settings


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

    def get_client(self):
        return boto3.client(
            's3',
            aws_access_key_id=self.config['aws_access_key_id'],
            aws_secret_access_key=self.config['aws_secret_access_key'],
            endpoint_url=self.config['endpoint_url']
        )

    def upload_file(self, filename: str, file_stream: io.BytesIO):
        client = self.get_client()
        try:
            client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=file_stream
            )
        except NoCredentialsError:
            print("Credentials not available")

    def download_file(self, filepath: str) -> io.BytesIO:
        client = self.get_client()
        try:
            response = client.get_object(
                Bucket=self.bucket_name,
                Key=filepath
            )
            file_stream = io.BytesIO(response['Body'].read())
            return file_stream
        except NoCredentialsError:
            print("Credentials not available")


s3_client = S3Client(
    access_key=settings.s3.access_key,
    secret_key=settings.s3.secret_key,
    endpoint_url=settings.s3.endpoint_url,
    bucket_name=settings.s3.bucket_name
)