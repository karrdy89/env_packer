from pydantic import BaseModel


class BaseContainerStats(BaseModel):
    CPU_USAGE: float | None = None
    MEM_USAGE: int | None = None
    MEM_LIMIT: int | None = None
    NET_IN: int | None = None
    NET_OUT: int | None = None
    DISK_IN: int | None = None
    DISK_OUT: int | None = None


class FullContainerStats(BaseContainerStats):
    STORAGE_USAGE: int | None = None


class BaseServerStats(BaseModel):
    HEALTHY: bool = False
    DETAILS: dict = {}
    SERVERS: list = []
