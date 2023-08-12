from pydantic import BaseModel
from datetime import datetime


class LineFile(BaseModel):
    data: str
    version: datetime = datetime.now()
    is_locked_by: str = ''
    released_at: datetime = datetime.now()


class FileData(BaseModel):
    name: str
    data: list[LineFile]
