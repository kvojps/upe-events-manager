import os
import sys
import tempfile
import threading
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from api.config.dynaconf import settings
from api.config.s3 import S3Config
from api.ports.file_handler import FileHandlerProvider

MB = 1024 * 1024


class TransferCallback:
    """
    Handle callbacks from the transfer manager.

    The transfer manager periodically calls the __call__ method throughout
    the upload and download process so that it can take action, such as
    displaying progress to the user and collecting data about the transfer.
    """

    def __init__(self, target_size):
        self._target_size = target_size
        self._total_transferred = 0
        self._lock = threading.Lock()
        self.thread_info = {}

    def __call__(self, bytes_transferred):
        """
        The callback method that is called by the transfer manager.

        Display progress during file transfer and collect per-thread transfer
        data. This method can be called by multiple threads, so shared instance
        data is protected by a thread lock.
        """
        thread = threading.current_thread()
        with self._lock:
            self._total_transferred += bytes_transferred
            if thread.ident not in self.thread_info.keys():
                self.thread_info[thread.ident] = bytes_transferred
            else:
                self.thread_info[thread.ident] += bytes_transferred

            target = self._target_size * MB
            sys.stdout.write(
                f"\r{self._total_transferred} of {target} carregado para o s3 "
                f"({(self._total_transferred / target) * 100:.2f}%)."
            )
            sys.stdout.flush()


class FileHandlerS3Adapter(FileHandlerProvider):
    def __init__(self):
        self._session = S3Config()
        self._bucket_name = settings.S3_BUCKET_NAME

    def put_object(self, file_to_upload: bytes, folder: str, key_obj: str) -> str:
        try:
            key = folder + "/" + key_obj
            self._session.s3_client().put_object(
                Body=file_to_upload,
                Bucket=self._bucket_name,
                Key=key,
            )

            return key
        except ClientError as e:
            raise e

    def multipart_object_upload(
        self, file_to_upload: bytes, folder: str, key_obj: str
    ) -> str:
        try:
            file_size_mb = len(file_to_upload) // (1024 * 1024)
            transfer_callback = TransferCallback(file_size_mb)
            config = TransferConfig(multipart_chunksize=1 * MB)
            key_obj = folder + "/" + key_obj

            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file_to_upload)
                temp_file_path = temp_file.name

            self._session.s3_client().upload_file(
                Filename=temp_file_path,
                Bucket=self._bucket_name,
                Key=key_obj,
                Callback=transfer_callback,
                Config=config,
            )
            transfer_callback.thread_info

            os.remove(temp_file_path)

            return key_obj
        except ClientError as e:
            raise e
