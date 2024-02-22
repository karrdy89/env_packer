import os
from dataclasses import dataclass
import configparser

from pydantic import BaseModel

ROOT_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

TEMP_DIR = ROOT_DIR + "/tmp"
PYTHON_VERSIONS = ["python3.11"]


class SystemEnvironments(BaseModel):
    NAME: str = "ENV_PACKER"
    VERIFY_SSL: bool
    API_SERVER: str
    WORKERS: int
    S3_ENDPOINT: str
    S3_ACCESS_KEY: str
    S3_SECRET_KEY: str
    SSL_KEY_FILE: str
    SSL_CERT_FILE: str
    SSL_CA_CERT_FILE: str
    PIP_INDEX: str
    PIP_INDEX_URL: str
    PIP_TRUSTED_HOST: str
    DISCOVER_URL: str
    DISCOVER_REGION: str
    DISCOVER_TAG: str


configs = configparser.ConfigParser(allow_no_value=True)
configs.read(ROOT_DIR + "/config/server_config.ini")
SYSTEM_ENV = SystemEnvironments(API_SERVER=configs["DEFAULT"]["API_SERVER"],
                                WORKERS=configs["DEFAULT"]["WORKERS"],
                                VERIFY_SSL=bool(int(configs["DEFAULT"]["VERIFY_SSL"])),
                                S3_ENDPOINT=configs["S3"]["ENDPOINT"],
                                S3_ACCESS_KEY=configs["S3"]["ACCESS_KEY"],
                                S3_SECRET_KEY=configs["S3"]["SECRET_KEY"],
                                SSL_KEY_FILE=configs["SSL"]["KEY_FILE"],
                                SSL_CERT_FILE=configs["SSL"]["CERT_FILE"],
                                SSL_CA_CERT_FILE=configs["SSL"]["CA_CERT_FILE"],
                                PIP_INDEX=configs["PIP"]["PIP_INDEX"],
                                PIP_INDEX_URL=configs["PIP"]["PIP_INDEX_URL"],
                                PIP_TRUSTED_HOST=configs["PIP"]["PIP_TRUSTED_HOST"],
                                DISCOVER_URL=configs["SERVICE_DISCOVER"]["URL"],
                                DISCOVER_REGION=configs["SERVICE_DISCOVER"]["REGION"],
                                DISCOVER_TAG=configs["SERVICE_DISCOVER"]["TAG"]
                                )


@dataclass
class RequestResult:
    SUCCESS: str = "00"
    FAIL: str = "10"


@dataclass
class RequestPath:
    REGISTER_SERVICE: str = "/api/v0/service/register"
    CHECK_SERVICE_CONNECTION: str = "/api/v0/service"


@dataclass
class ModelStore:
    BASE_PATH: str = "models"

