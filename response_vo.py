from pydantic import BaseModel


class Base(BaseModel):
    CODE: str
    ERROR_MSG: str


class ListBackends(Base):
    BACKENDS: list[str]
