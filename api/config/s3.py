import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from api.config.dynaconf import settings


class S3Config:
    def __init__(self):
        self._region = settings.AWS_REGION
        self._aws_access_key_id = settings.AWS_ACCESS_KEY_ID
        self._aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY

    def s3_client(self) -> BaseClient:
        try:
            s3 = boto3.client(
                "s3",
                self._region,
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key,
            )
            return s3

        except ClientError as e:
            raise e
