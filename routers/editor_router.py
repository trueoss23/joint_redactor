from fastapi import APIRouter
from dto.file import FileData

router = APIRouter(prefix='/editor')

db = []


@router.get('/files')
def show_files():
    return db


@router.post('/file', status_code=201)
async def create_file(new_file: FileData):
    db.append(new_file)
