from io import BytesIO
from typing import Optional

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
from mypy_boto3_s3 import S3Client, S3ServiceResource
from mypy_boto3_s3.type_defs import (
    CopySourceTypeDef,
    DeleteTypeDef,
    ObjectIdentifierTypeDef,
)


class AwsWrapper:
    _client: S3Client
    _resource = S3ServiceResource

    def __init__(self, key: Optional[str] = None, secret: Optional[str] = None):

        wrapper_config = Config(
            region_name="us-east-2",
        )

        if key and secret:
            self._client = boto3.client(
                "s3",
                aws_access_key_id=key,
                aws_secret_access_key=secret,
                config=wrapper_config,
            )
            self._resource = boto3.resource(
                "s3",
                aws_access_key_id=key,
                aws_secret_access_key=secret,
                config=wrapper_config,
            )
        else:
            self._client = boto3.client("s3", config=wrapper_config)
            self._resource = boto3.resource("s3", config=wrapper_config)

    def upload_file(
        self,
        bucket_name: str,
        origin_path: str,
        destination_path: str,
    ):
        self._client.upload_file(
            origin_path,
            bucket_name,
            destination_path,
        )

    def upload_file_object(
        self,
        bucket_name: str,
        file_object: BytesIO,
        destination_path: str,
    ):
        self._client.upload_fileobj(
            file_object,
            bucket_name,
            destination_path,
        )

    def check_file_exists(
        self,
        bucket_name: str,
        file_path: str,
    ) -> bool:
        try:
            self._client.head_object(
                Bucket=bucket_name,
                Key=file_path,
            )
        except ClientError:
            try:
                respons = self._client.list_objects_v2(
                    Bucket=bucket_name,
                    Prefix=file_path,
                )
                if "Contents" not in respons:
                    return False

            except ClientError:
                return False
        return True

    def list_files(
        self,
        bucket_name: str,
        prefix: str = "",
    ) -> list[str]:
        response = self._client.list_objects_v2(
            Bucket=bucket_name,
            Prefix=prefix,
        )
        if "Contents" not in response:
            return []

        files = [
            object_key
            for object_key in [
                obj.get("Key") or ""
                for obj in response.get("Contents", [])
                if obj.get("Key")
            ]
            if "temp" not in object_key
        ]

        return files

    def delete_file(
        self,
        bucket_name: str,
        file_path: str,
    ):
        self._client.delete_object(
            Bucket=bucket_name,
            Key=file_path,
        )

    def delete_object(
        self,
        bucket_name: str,
        directory_name: str,
    ):
        if directory_name[-1] == "/":
            objects_to_delete = self.list_files(
                bucket_name=bucket_name,
                prefix=directory_name,
            )
            for obj in objects_to_delete:
                self.delete_object(
                    bucket_name=bucket_name,
                    directory_name=obj,
                )
            return

        self._client.delete_object(
            Bucket=bucket_name,
            Key=directory_name,
        )

    def delete_directory_limit(
        self,
        bucket_name: str,
        directory_path: str,
    ):
        objects_to_delete = self._client.list_objects(
            Bucket=bucket_name,
            Prefix=directory_path,
        )

        delete = DeleteTypeDef(
            Objects=[
                ObjectIdentifierTypeDef(
                    Key=k,
                )
                for k in [
                    obj.get("Key") or ""
                    for obj in objects_to_delete.get("Contents", [])
                    if obj.get("Key")
                ]
            ]
        )

        self._client.delete_objects(
            Bucket=bucket_name,
            Delete=delete,
        )

    def delete_directory(
        self,
        bucket_name: str,
        directory_path: str,
    ):
        paginator = self._client.get_paginator("list_objects_v2")

        page_iterator = paginator.paginate(
            Bucket=bucket_name,
            Prefix=directory_path,
        )
        delete_keys = DeleteTypeDef(
            Objects=[
                ObjectIdentifierTypeDef(Key=k)
                for k in [
                    obj.get("Key") or ""
                    for obj in [
                        obj
                        for page in page_iterator.search("Contents")
                        for obj in page.get("Contents", [])
                    ]
                ]
            ]
        )

        self._client.delete_objects(
            Bucket=bucket_name,
            Delete=delete_keys,
        )

    def create_dir(
        self,
        bucket_name: str,
        dir_path: str,
    ):
        self._client.put_object(
            Bucket=bucket_name,
            Key=dir_path,
        )

    def check_dir_exists(
        self,
        bucket_name: str,
        dir_path: str,
    ) -> bool:
        try:
            self._client.head_object(
                Bucket=bucket_name,
                Key=dir_path,
            )
        except ClientError:
            return False
        return True

    def read_file(
        self,
        bucket_name: str,
        file_path: str,
    ):
        file_object = self._client.get_object(
            Bucket=bucket_name,
            Key=file_path,
        )
        return file_object["Body"].read()

    def moove_file(
        self,
        bucket_name: str,
        origin_path: str,
        destination_path: str,
    ):
        self._client.copy_object(
            Bucket=bucket_name,
            CopySource=f"{bucket_name}/{origin_path}",
            Key=destination_path,
        )
        self._client.delete_object(
            Bucket=bucket_name,
            Key=origin_path,
        )

    def create_presigned_url(
        self,
        bucket_name: str,
        object_name: str,
        expiration: int = 3600,
    ) -> str:
        response = self._client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket_name,
                "Key": object_name,
            },
            ExpiresIn=expiration,
        )
        return response

    def list_objects(self, bucket_name: str, prefix_path: str):
        response = self._client.list_objects_v2(Bucket=bucket_name, Prefix=prefix_path)
        return response

    def download_file(self, bucket, key, filename):
        self._client.download_file(Bucket=bucket, Key=key, Filename=filename)

    def download_fileobj(self, bucket, key, fileobj):
        self._client.download_fileobj(Bucket=bucket, Key=key, Fileobj=fileobj)

    def upload_file_bytes(
        self,
        bucket_name: str,
        file_bytes: bytes,
        destination_path: str,
    ):
        self._client.put_object(
            Body=file_bytes,
            Bucket=bucket_name,
            Key=destination_path,
        )

    def rename_file(
        self,
        bucket_name: str,
        old_path: str,
        new_path: str,
    ):
        copy_source = CopySourceTypeDef(
            Bucket=bucket_name,
            Key=old_path,
        )

        self._client.copy_object(
            Bucket=bucket_name,
            CopySource=copy_source,
            Key=new_path,
        )
        self._client.delete_object(
            Bucket=bucket_name,
            Key=old_path,
        )
