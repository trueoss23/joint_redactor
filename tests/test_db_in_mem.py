from fastapi.testclient import TestClient
from fastapi import status
from fastapi.encoders import jsonable_encoder

import json

from main import app
from dto.file import LineFile
import constants as c

client = TestClient(app=app)


def test_read_files_succes_empty_db():
    response = client.get('/editor/files')
    data = json.loads(response.content)
    print(data)
    assert response.status_code == status.HTTP_200_OK
    assert type(data) == list
    assert len(data) == 0


def test_read_files_succes(db_mem):
    response = client.get('/editor/files')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert type(data) == list
    assert len(data) == 1


def test_read_file_succes(db_mem):
    response = client.get(f'/editor/{c.filename1}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert data['name'] == c.filename1
    assert data['data'][0]['line'] == c.file1.data[0].line
    assert data['data'][1]['line'] == c.file1.data[1].line


def test_read_file_NoFilenameInDb_404(db_mem):
    response = client.get(f'editor/{c.filename2}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_read_line_succes(db_mem):
    response = client.get(f'editor/{c.filename1}/{0}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert data['line'] == c.line1


def test_read_line_NoFilenameInDb_404(db_mem):
    response = client.get(f'editor/{c.filename2}/{c.num_line1}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_read_line_ErrorNumLine_404(db_mem):
    response = client.get(f'editor/{c.filename1}/{3}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.num_line_not_exists} line in {c.filename1}'


def test_add_file_succes(db_mem):
    json_data = jsonable_encoder(dict(c.file2))
    response = client.post('editor/file', json=json_data)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_201_CREATED
    assert data == c.filename2


def test_add_file_FilenameAlreadyExists_409(db_mem):
    json_data = jsonable_encoder(dict(c.file1))
    response = client.post('editor/file', json=json_data)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert data['detail'] == f'{c.filename1} is already exists'


def test_add_line_succes(db_mem):
    json_data = jsonable_encoder(LineFile(line=c.line3))
    response = client.post(f'/editor/{c.filename1}/line', json=json_data)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_201_CREATED
    assert data == 2


def test_add_line_NoFilenameInDb_404(db_mem):
    json_data = jsonable_encoder(LineFile(line=c.line3))
    response = client.post(f'/editor/{c.filename2}/line', json=json_data)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_update_line_succes(db_mem):
    json_data = jsonable_encoder(LineFile(line=c.line3))
    response = client.patch(f'editor/{c.filename1}/{c.num_line1}', json=json_data)
    assert response.status_code == status.HTTP_200_OK


def test_update_line_NoFilenameInDb_404(db_mem):
    json_data = jsonable_encoder(LineFile(line=c.line3))
    response = client.patch(f'editor/{c.filename2}/{c.num_line1}', json=json_data)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_update_line_ErrorNumLine_404(db_mem):
    json_data = jsonable_encoder(LineFile(line=c.line3))
    response = client.patch(f'editor/{c.filename1}/{c.num_line_not_exists}', json=json_data)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.num_line_not_exists} line in {c.filename1}'


def test_update_line_NoDateForUpdate_304(db_mem):
    json_data = jsonable_encoder(LineFile(line=c.line1))
    response = client.patch(f'editor/{c.filename1}/{c.num_line1}', json=json_data)
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_delete_line_succes(db_mem):
    response = client.delete(f'editor/{c.filename1}/{c.num_line1}')
    assert response.status_code == status.HTTP_200_OK


def test_delete_line_NoFilenameInDb_404(db_mem):
    response = client.delete(f'editor/{c.filename2}/{c.num_line1}')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_line_ErrorNumLine_404(db_mem):
    response = client.delete(f'editor/{c.filename1}/{c.num_line_not_exists}')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_file_succes(db_mem):
    response = client.delete(f'editor/{c.filename1}')
    assert response.status_code == status.HTTP_200_OK


def test_delete_file_NoFilenameInDb_404(db_mem):
    response = client.delete(f'editor/{c.filename2}')
    assert response.status_code == status.HTTP_404_NOT_FOUND
