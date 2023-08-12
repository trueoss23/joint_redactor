from pydantic import BaseModel
from datetime import datetime


class LineFile(BaseModel):
    version: datetime = datetime.now()
    is_locked_by: str = 'Igor'
    released_at: datetime = datetime.now()


class FileData(BaseModel):
    name: str = 'test'
    data: list[LineFile]
