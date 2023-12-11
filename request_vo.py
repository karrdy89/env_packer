from pydantic import BaseModel


class UploadEnv(BaseModel):
    PRJ_ID: str
    CONVERTER_ID: str
    PYTHON_VER: str | None = None
    PACKAGES: list[str]
