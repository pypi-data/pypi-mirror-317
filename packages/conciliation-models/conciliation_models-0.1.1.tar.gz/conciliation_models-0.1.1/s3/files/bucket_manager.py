import os
from io import BytesIO
from typing import Optional

from fastapi import UploadFile
from loggerk import LoggerK

from s3.files.aws_wrapper import AwsWrapper
from s3.files.file_manager import FileManager
from tools.env import env
from fastapi import HTTPException

class BucketManager:
    _logger: LoggerK
    _aws_wrapper: AwsWrapper
    _bucket: str
    _bucket_root: str

    def __init__(
        self,
        aws_key: Optional[str] = None,
        aws_secret: Optional[str] = None,
        aws_bucket_name: str = env.AWS_BUCKET_NAME,
        bucket_root: str = os.path.join(env.BUCKET_ROOT, env.DEV_MODE),
    ):
        self._logger = LoggerK(self.__class__.__name__)
        AWS_BUCKET_KEY = aws_key or env.AWS_BUCKET_KEY
        AWS_BUCKET_SECRET = aws_secret or env.AWS_BUCKET_SECRET

        self._aws_wrapper = AwsWrapper(
            key=AWS_BUCKET_KEY,
            secret=AWS_BUCKET_SECRET,
        )
        self._bucket_root = bucket_root
        self._bucket = aws_bucket_name

    def get_path(
        self,
        directory_name: str,
        file_name: Optional[str] = None,
    ) -> str:
        # remove the bucket root if it is already in the path
        directory_name = directory_name.replace(self._bucket_root, "", 1)

        while directory_name.startswith("/"):
            directory_name = directory_name.removeprefix("/")
        path = os.path.join(self._bucket_root, directory_name)
        if file_name:
            path = os.path.join(path, file_name)
        return path

    def create_directory(self, directory_name: str) -> None:
        self._logger.info(f"Creating directory {directory_name}")
        new_directory = self.get_path(directory_name)

        self._aws_wrapper.create_dir(
            bucket_name=self._bucket,
            dir_path=new_directory,
        )
        self._logger.info(f"Directory {directory_name} created successfully")

    def delete_dir(self, directory_name: str) -> None:
        self._logger.info(f"Deleting directory {directory_name}")
        new_directory = self.get_path(directory_name)

        self._aws_wrapper.delete_object(
            bucket_name=self._bucket,
            directory_name=new_directory,
        )
        self._logger.info(f"Directory {directory_name} deleted successfully")

    def upload_file(
        self,
        origin_path: str,
        destination_path: str,
    ) -> str:
        """
        Uploads a file from the origin path to the destination path in the bucket.

        Args:
            origin_path (str): The path of the file to be uploaded.
            destination_path (str): The path where the file will be stored in the bucket.

        Returns:
            str: The final path of the file in the bucket.

        """
        self._logger.info(f"Uploading file {origin_path}")
        destination_path = self.get_path(destination_path)
        self._aws_wrapper.upload_file(
            bucket_name=self._bucket,
            origin_path=origin_path,
            destination_path=destination_path,
        )
        self._logger.info(f"File {origin_path} uploaded successfully")

        # url = self._aws_wrapper.create_presigned_url(
        #     bucket_name=self._bucket,
        #     object_name=destination_path,
        # )
        # return url
        return destination_path

    def upload_file_from_bytes(
        self,
        file_bytes: BytesIO,
        destination_path: str,
    ) -> str:
        self._logger.info("Uploading file from bytes")
        destination_path = self.get_path(destination_path)
        self._aws_wrapper.upload_file_object(
            bucket_name=self._bucket,
            file_object=file_bytes,
            destination_path=destination_path,
        )
        self._logger.info("File uploaded successfully")

        # url = self._aws_wrapper.create_presigned_url(
        #     bucket_name=self._bucket,
        #     object_name=destination_path,
        # )
        # return url
        return destination_path

    def download_file(
        self,
        file_path: str,
    ) -> str:
        self._logger.info(f"Downloading file {file_path}")
        bucket_file_path = self.get_path(file_path)

        if not self.check_path_exists(file_path):
            message = f"File {file_path} does not exists"
            self._logger.error(message)
            raise HTTPException(status_code=404, detail=message)

        url = self._aws_wrapper.create_presigned_url(
            bucket_name=self._bucket,
            object_name=bucket_file_path,
        )
        self._logger.info(f"File {file_path} downloaded successfully")
        return url

    def download_file_local(
        self,
        bucket_path: str,
        local_path: str,
        file_manager: FileManager = FileManager(),
    ) -> str:
        self._logger.info(f"Downloading file {bucket_path}")
        local_path = file_manager.get_path(local_path)
        bucket_path = self.get_path(bucket_path)

        if not os.path.exists(os.path.dirname(local_path)):
            os.makedirs(os.path.dirname(local_path))

        self._aws_wrapper.download_file(
            bucket=self._bucket, key=bucket_path, filename=local_path
        )

        self._logger.info("Successful download")
        return local_path

    def list_all_path(self, file_path) -> list[str]:
        self._logger.info("Listando todas las rutas")
        file_path = self.get_path(file_path)
        paths_files = self._aws_wrapper.list_files(
            bucket_name=self._bucket, prefix=file_path
        )
        if not paths_files:
            return []
        return paths_files

    def download_first_file(
        self,
        directory_name: str,
    ) -> str:
        # return the first file in the directory
        self._logger.info(f"Downloading first file in {directory_name}")
        bucket_directory_path = self.get_path(directory_name)

        if not self.check_path_exists(directory_name):
            message = f"El directorio {directory_name} no existe"
            self._logger.error(message)
            raise FileNotFoundError(message)

        first_file = self._aws_wrapper.list_files(
            bucket_name=self._bucket,
            prefix=bucket_directory_path,
        )[0]
        if not first_file:
            message = f"Directorio {directory_name} vacío"
            self._logger.error(message)
            raise FileNotFoundError(message)

        url = self._aws_wrapper.create_presigned_url(
            bucket_name=self._bucket,
            object_name=first_file,
        )
        return url

    def check_path_exists(
        self,
        directory_name: str,
        file_name: Optional[str] = None,
    ) -> bool:
        path = self.get_path(directory_name, file_name)
        return self._aws_wrapper.check_file_exists(
            bucket_name=self._bucket,
            file_path=path,
        )

    def rename_file(
        self,
        directory_name: str,
        old_file_name: str,
        new_file_name: str,
    ) -> None:
        self._logger.info(f"Renaming file {old_file_name} to {new_file_name}")
        old_path = self.get_path(directory_name, old_file_name)
        new_path = self.get_path(directory_name, new_file_name)

        self._aws_wrapper.rename_file(
            bucket_name=self._bucket,
            old_path=old_path,
            new_path=new_path,
        )
        self._logger.info("File renamed successfully")

    def upload_fastapi_file(
        self,
        file: UploadFile,
        destination_path: str,
        file_manager: FileManager = FileManager(),
    ) -> str:
        self._logger.info(f"Uploading file {file.filename}")
        destination_path = self.get_path(destination_path, file.filename)

        local_path = os.path.join(
            "uploads",
            file.filename or "",
        )

        local_file = file_manager.upload_fastapi_file(
            file=file,
            destination_path=local_path,
        )

        try:
            self.upload_file(
                origin_path=local_file,
                destination_path=destination_path,
            )
        finally:
            file_manager.delete_dir("uploads")

        final_path = self.get_path(destination_path)

        return final_path

    def create_presigned_url(
        self,
        directory_name: str,
        file_name: Optional[str] = None,
    ) -> str:
        path = self.get_path(directory_name, file_name)
        return self._aws_wrapper.create_presigned_url(
            bucket_name=self._bucket,
            object_name=path,
        )
