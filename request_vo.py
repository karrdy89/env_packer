from pydantic import BaseModel, Extra

from _types import BaseServerStats


class UploadEnv(BaseModel):
    PRJ_ID: str
    CONVERTER_ID: str
    PATH: str
    PYTHON_VER: str
    PACKAGES: list[str]


class RegisterService(BaseModel):
    URL: str
    LABEL: str
    TAG: str | None = None
    REGION: str | None = None
    TOKEN: str | None = None
    HEALTH_CHECK_PATH: str | None = None

    class Config:
        extra = Extra.forbid


class ServerStat(BaseModel):
    NAME: str
    STATS: BaseServerStats


class ServerStats(BaseModel):
    SERVER_STATS: ServerStat
    REGION: str | None = None
    INTERVAL: int
    URL: str
