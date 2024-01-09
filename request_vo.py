from pydantic import BaseModel, Extra


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
    TOKEN: bytes | None = None
    REGION: str
    ID: str

    class Config:
        extra = Extra.forbid
