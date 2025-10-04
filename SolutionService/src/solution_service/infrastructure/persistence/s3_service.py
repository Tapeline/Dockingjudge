import json
import logging
from dataclasses import dataclass
from io import BytesIO
from urllib.parse import urlsplit

import minio
from dishka import FromDishka

from solution_service.application.interfaces.storage import URL, File, Storage
from solution_service.config import Config


@dataclass
class S3ConnectionParameters:
    bucket_name: str
    endpoint: str
    username: str
    password: str
    is_secure: bool


class S3Storage(Storage):
    client: minio.Minio | None

    def __init__(self, config: FromDishka[Config]) -> None:
        self.client = None
        self.params = S3ConnectionParameters(
            bucket_name=config.s3.bucket_name,
            endpoint="{host}:{port}".format(
               host=config.s3.host
               .replace("https://", "")
               .replace("http://", ""),
               port=config.s3.port,
            ),
            username=config.s3.username,
            password=config.s3.password,
            is_secure=config.s3.host.startswith("https"),
        )
        self.logger = logging.getLogger("s3")
        self.connect()
        self.create_bucket_if_not_present()

    def create_bucket_if_not_present(self) -> None:
        if not self.client.bucket_exists(self.params.bucket_name):
            self.logger.info("Bucket not found, creating")
            self.client.make_bucket(self.params.bucket_name)
            self.client.set_bucket_policy(
                self.params.bucket_name,
                json.dumps({
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": [
                                "s3:GetBucketLocation", "s3:ListBucket",
                            ],
                            "Resource": (
                                f"arn:aws:s3:::{self.params.bucket_name}"
                            ),
                        },
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": "s3:GetObject",
                            "Resource": (
                                f"arn:aws:s3:::{self.params.bucket_name}/*"
                            ),
                        },
                    ],
                }),
            )

    def connect(self) -> None:
        self.logger.info("Connecting to S3")
        self.client = minio.Minio(
            self.params.endpoint,
            access_key=self.params.username,
            secret_key=self.params.password,
            secure=self.params.is_secure,
        )

    async def get_file_url(self, name: str) -> URL:
        self.logger.info("Getting file url for %s", name)
        signed_url = self.client.get_presigned_url(
            "GET", self.params.bucket_name, name,
        )
        url = urlsplit(signed_url)
        return url.path

    async def save_file(self, file: File) -> URL:
        self.logger.info("Saving file %s", file.name)
        fake_io = BytesIO(file.contents)
        self.client.put_object(
            bucket_name=self.params.bucket_name,
            object_name=file.name,
            data=fake_io,
            length=len(file.contents),
        )
        return await self.get_file_url(file.name)

    async def get_file(self, url: URL) -> File:
        self.logger.info("Getting file by url %s", url)
        url = url.removeprefix("/").removesuffix("/")
        bucket_name, object_id = url.split("/")
        response = None
        try:
            response = self.client.get_object(bucket_name, object_id)
            return File(
                name=object_id,
                contents=response.read(),
            )
        finally:
            if response is not None:
                response.close()
                response.release_conn()
            raise
