import os
import tempfile
import threading
import time
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError
from api.config.s3 import S3Config
from api.utils.progress_checker import ProgressChecker
from core.infrastructure.settings.env_handler import settings
from core.infrastructure.shared.cloud.file_handler import FileHandlerProvider

MB = 1024 * 1024


class TransferCallback:
    """
    Handle callbacks from the transfer manager.

    The transfer manager periodically calls the __call__ method throughout
    the upload and download process so that it can take action, such as
    displaying progress to the user and collecting data about the transfer.
    """

    def __init__(self, target_size: int, detail: str):
        self._detail = detail
        self._start_time = time.time()
        self._target_size = target_size
        self._total_transferred = 0
        self._lock = threading.Lock()
        self.thread_info = {}  # type: ignore

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

            ProgressChecker.get_progress(
                self._detail, self._total_transferred, target, self._start_time
            )


class FileHandlerS3Adapter(FileHandlerProvider):
    def __init__(self):
        self._session = S3Config()
        self._bucket_name = settings.S3_BUCKET_NAME

    def download_object(self, key: str, download_file_path: str) -> None:
        try:
            self._session.s3_client().download_file(
                self._bucket_name, key, download_file_path
            )
        except ClientError as e:
            raise e

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
            transfer_callback = TransferCallback(
                file_size_mb, "Progresso multipart upload"
            )
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
