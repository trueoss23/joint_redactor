from fastapi import APIRouter, HTTPException, status

from dto.file import FileData, LineFile
from common.exceptions import NoFilenameInDb, ErrorNumLine, FilenameAlreadyExists, NoDateForUpdate
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
    except (NoFilenameInDb) as e:
        raise HTTPException(status_code=404,
                            detail=str(e))
    return result


@router.get('/{filename}/{num_line}')
async def read_line(filename: str, num_line: int):
    try:
        result = di.db.read_line(filename, num_line)
    except (NoFilenameInDb, ErrorNumLine) as e:
        raise HTTPException(status_code=404,
                            detail=str(e))
    return result


@router.post('/file', status_code=201)
async def create_file(new_file: FileData):
    try:
        result = di.db.create_file(new_file)
    except FilenameAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=str(e))
    return result


@router.post('/{filename}/line', status_code=201)
async def add_line(filename: str, line: LineFile):
    try:
        result = di.db.add_line(filename, line)
    except NoFilenameInDb as e:
        raise HTTPException(status_code=404,
                            detail=str(e))
    return result


@router.patch('/{filename}/{num_line}')
async def update_line(filename: str, num_line: int, new_line: LineFile):
    try:
        di.db.update_line(filename, num_line, new_line)
    except (NoFilenameInDb, ErrorNumLine) as e:
        raise HTTPException(status_code=404,
                            detail=str(e))
    except NoDateForUpdate:
        raise HTTPException(status_code=304)
    return


@router.delete('/{filename}/{num_line}')
async def delete_line(filename: str, num_line: int):
    try:
        di.db.delete_line(filename, num_line)
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
