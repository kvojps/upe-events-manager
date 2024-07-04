import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError
from core.infrastructure.settings.env_handler import settings


class SESConfig:
    def __init__(self):
        self._region = settings.REGION
        self._aws_access_key_id = settings.ACCESS_KEY_ID
        self._aws_secret_access_key = settings.SECRET_ACCESS_KEY

    def ses_client(self) -> BaseClient:
        try:
            ses = boto3.client(
                "ses",
                self._region,
                aws_access_key_id=self._aws_access_key_id,
                aws_secret_access_key=self._aws_secret_access_key,
            )
            return ses

        except ClientError as e:
            raise e
