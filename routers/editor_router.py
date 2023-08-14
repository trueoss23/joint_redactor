from fastapi import APIRouter, HTTPException

from dto.file import FileData
from common.exceptions import NoFilenameInDb, ErrorNumLine, FilenameAlreadyExists
from di_container import get_di_container

router = APIRouter(prefix='/editor')
di = get_di_container()


@router.get('/files')
async def read_files():
    return di.db.read_files()


@router.get('/{filename}')
async def read_file(filename: str):
    try:
        result = di.db.read_file(filename)
    except (NoFilenameInDb, ErrorNumLine) as e:
        raise HTTPException(status_code=404,
                            detail=str(e))
    return result


@router.get('/{filename}/{num_line}')
async def read_line(filename: str, num_line: int):
    try:
        di.db.read_line(filename, num_line)
    except (NoFilenameInDb, ErrorNumLine) as e:
        raise HTTPException(status_code=404,
                            detail=str(e))


@router.post('/file', status_code=201)
async def create_file(new_file: FileData):
    try:
        di.db.create_file(new_file)
    except FilenameAlreadyExists as e:
        raise HTTPException(status_code=409,
                            detail=str(e))


@router.post('/{filename}')
async def add_line(line: str):
    try:
        di.db.add_line(line)
    except NoFilenameInDb as e:
        raise HTTPException(status_code=404,
                            detail=str(e))


@router.patch('/{filename}/{num_line}')
async def update_line(filename: str, num_line: int):
    try:
        di.db.update_line(filename, num_line)
    except (NoFilenameInDb, ErrorNumLine) as e:
        raise HTTPException(status_code=404,
                            detail=str(e))


@router.delete('/{filename}/{num_line}')
async def delete_line(filename: str, num_line: int):
    try:
        di.db.delete_file(filename, num_line)
    except (NoFilenameInDb, ErrorNumLine) as e:
        raise HTTPException(status_code=404,
                            detail=str(e))


@router.delete('/{filename}')
async def delete_file(filename: str):
    try:
        di.db.delete_file(filename)
    except NoFilenameInDb as e:
        raise HTTPException(status_code=404,
                            detail=str(e))
