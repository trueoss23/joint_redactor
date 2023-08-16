from pydantic import BaseModel


class FileData(BaseModel):
    name: str
    data: list[str]
