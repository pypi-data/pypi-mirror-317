import os
from io import BytesIO
from pathlib import Path
from shutil import rmtree
from typing import BinaryIO, Optional

from fastapi import BackgroundTasks, UploadFile
from loggerk import LoggerK


class FileManager:
    _logger: LoggerK

    def __init__(self):
        self._logger = LoggerK(self.__class__.__name__)
        self._local_files_root = "tmp"

    def get_path(
        self,
        directory_name: str,
        file_name: Optional[str] = None,
    ) -> str:
        # check if directory_name already has the root
        if directory_name.startswith(self._local_files_root):
            return directory_name
        path = os.path.join(
            os.getcwd(),
            self._local_files_root,
            directory_name,
        )
        if file_name:
            path = os.path.join(path, file_name)
        return path

    def get_list_directory(self, directory: str) -> list[str]:
        self._logger.info(f"Getting list of directory {directory}")
        local_dir = self.get_path(directory)

        return os.listdir(local_dir)

    def upload_file(
        self,
        file_upload: BinaryIO,
        destination_path: str,
        new_name: Optional[str] = None,
    ) -> str:
        self._logger.info(f"Uploading file {file_upload.name} to {destination_path}")
        local_dir = self.get_path(destination_path)
        content = file_upload.read()
        new_name = new_name or str(file_upload.name)
        new_directory = os.path.join(local_dir, new_name)

        if not os.path.exists(os.path.dirname(new_directory)):
            os.makedirs(os.path.dirname(new_directory))

        with open(new_directory, "wb") as f:
            f.write(content)
        self._logger.info(f"File {file_upload.name} uploaded successfully")
        return new_directory

    def upload_file_from_bytes(
        self,
        file_bytes: BinaryIO,
        destination_path: str,
    ) -> str:
        self._logger.info("Uploading file from bytes")
        destination_path = self.get_path(destination_path)
        new_directory = destination_path

        if not os.path.exists(os.path.dirname(new_directory)):
            os.makedirs(os.path.dirname(new_directory))

        with open(new_directory, "wb") as f:
            readable_buffer = file_bytes.read()
            f.write(readable_buffer)
        self._logger.info("File uploaded successfully")
        return new_directory

    def upload_fastapi_file(
        self,
        file: UploadFile,
        destination_path: str,
        new_name: Optional[str] = None,
    ) -> str:
        self._logger.info(f"Uploading file {file.filename} to {destination_path}")

        file_name = new_name or file.filename

        new_directory = self.upload_file(
            file_upload=file.file,
            destination_path=destination_path,
            new_name=file_name,
        )

        self._logger.info(f"File {file_name} uploaded successfully")
        return new_directory

    def create_directory(self, directory_name: str) -> str:
        self._logger.info(f"Creating directory {directory_name}")
        new_directory = self.get_path(directory_name)

        path = Path(new_directory)
        path.mkdir(parents=True, exist_ok=True)
        self._logger.info(f"Directory {directory_name} created successfully")
        return new_directory

    def get_file(
        self,
        file_path: str,
    ) -> BytesIO:
        self._logger.info(f"Getting file {file_path}")
        file_path = self.get_path(file_path)

        with open(file_path, "rb") as f:
            content = f.read()

        result = BytesIO(content)
        result.name = os.path.basename(file_path)
        self._logger.info(f"File {file_path} read successfully")
        return BytesIO(content)

    def delete_file(
        self,
        file_path: str,
    ) -> None:
        self._logger.info(f"Deleting file {file_path}")
        file_path = self.get_path(file_path)

        exists = os.path.isfile(file_path)
        if exists:
            os.remove(file_path)

        self._logger.info(f"File {file_path} deleted successfully")

    def delete_dir(
        self,
        directory_name: str,
    ) -> None:
        self._logger.info(f"Deleting directory {directory_name}")
        new_directory = self.get_path(directory_name)

        exists = os.path.isdir(new_directory)
        if exists:
            rmtree(new_directory)

        self._logger.info(f"Directory {directory_name} deleted successfully")

    def check_dir_exists(
        self,
        directory_name: str,
    ) -> bool:
        self._logger.info(f"Checking if directory {directory_name} exists")
        new_directory = self.get_path(directory_name)

        exists = os.path.isdir(new_directory)

        self._logger.info(f"Directory {directory_name} exists: {exists}")
        return exists

    def upload_from_bytes_and_schedule_delete(
        self,
        file_bytes: bytes,
        file_name: str,
        background_tasks: BackgroundTasks,
    ):
        readable_buffer = BytesIO(file_bytes)
        local_path = self.upload_file_from_bytes(
            file_bytes=readable_buffer,
            destination_path=file_name,
        )

        background_tasks.add_task(self.delete_file, local_path)
        return local_path
