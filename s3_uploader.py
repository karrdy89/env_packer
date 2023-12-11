import boto3
from boto3_type_annotations.s3 import Client
from smart_open import open as s_open

from _constants import SYSTEM_ENV


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class S3Uploader:
    def __init__(self, chunk_size: int = 50):
        self._chunk_size = chunk_size
        self._s3: Client = boto3.client(service_name="s3",
                                        endpoint_url=SYSTEM_ENV.S3_ENDPOINT,
                                        aws_access_key_id=SYSTEM_ENV.S3_ACCESS_KEY,
                                        aws_secret_access_key=SYSTEM_ENV.S3_SECRET_KEY,
                                        use_ssl=True,
                                        verify=False
                                        )

    def upload(self, bucket: str, source_path: str, target_path: str):
        url = f"s3://{bucket}/{target_path}"
        with open(source_path, "rb") as f_out:
            with s_open(url, "wb", transport_params={"client": self._s3}) as f_in:
                data = f_out.read(1024*1024*self._chunk_size)
                while data:
                    f_in.write(data)
                    data = f_out.read(1024*1024*self._chunk_size)
