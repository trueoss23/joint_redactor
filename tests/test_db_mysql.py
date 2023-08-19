from fastapi.testclient import TestClient
from fastapi import status
from fastapi.encoders import jsonable_encoder

import json

from main import app
import constants as c


client = TestClient(app=app)


def test_read_files_succes(db_mysql):
    response = client.get('/editor/files')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert len(data) == 1


def test_read_file_succes(db_mysql):
    response = client.get(f'/editor/{c.filename1}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert data['name'] == c.filename1
    assert data['data'][0]['line'] == c.file1.data[0]
    assert data['data'][1]['line'] == c.file1.data[1]


def test_read_file_NoFilenameInDb_404(db_mysql):
    response = client.get(f'editor/{c.filename2}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_read_line_succes(db_mysql):
    response = client.get(f'editor/{c.filename1}/{0}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert data['line'] == c.line1


def test_read_line_NoFilenameInDb_404(db_mysql):
    response = client.get(f'editor/{c.filename2}/{c.num_line1}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_read_line_ErrorNumLine_404(db_mysql):
    response = client.get(f'editor/{c.filename1}/{3}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.num_line_not_exists} line in {c.filename1}'


def test_add_file_succes(db_mysql):
    json_data = jsonable_encoder(dict(c.file2))
    response = client.post('editor/file', json=json_data)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_201_CREATED
    assert data == c.file2_id


def test_add_file_FilenameAlreadyExists_409(db_mysql):
    json_data = jsonable_encoder(dict(c.file1))
    response = client.post('editor/file', json=json_data)
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert data['detail'] == f'{c.filename1} is already exists'


def test_add_line_succes(db_mysql):
    response = client.patch(f'editor/{c.filename1}', params={'line': c.line3})
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    assert data == 2


def test_add_line_NoFilenameInDb_404(db_mysql):
    response = client.patch(f'editor/{c.filename2}', params={'line': c.line3})
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_update_line_succes(db_mysql):
    response = client.patch(f'editor/{c.filename1}/{c.num_line1}', params={'new_line': c.line3})
    assert response.status_code == status.HTTP_200_OK


def test_update_line_NoFilenameInDb_404(db_mysql):
    response = client.patch(f'editor/{c.filename2}/{c.num_line1}', params={'new_line': c.line3})
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_update_line_ErrorNumLine_404(db_mysql):
    response = client.patch(f'editor/{c.filename1}/{c.num_line_not_exists}', params={'new_line': c.line3})
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.num_line_not_exists} line in {c.filename1}'


def test_update_line_NoDateForUpdate_304(db_mysql):
    response = client.patch(f'editor/{c.filename1}/{c.num_line1}', params={'new_line': c.line1})
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_lock_line_succes(db_mysql):
    response1 = client.patch(f'editor/{c.filename1}/{c.num_line1}/lock')
    response2 = client.get(f'editor/{c.filename1}/{c.num_line1}')
    data = json.loads(response2.content)

    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK
    assert data['is_locked']


def test_lock_line_NoFile_404(db_mysql):
    response = client.patch(f'editor/{c.filename2}/{c.num_line1}/lock')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_lock_line_NoLine_404(db_mysql):
    response = client.patch(f'editor/{c.filename1}/{c.num_line_not_exists}/lock')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.num_line_not_exists} line in {c.filename1}'


def test_lock_line_NoDateForUpdate_304(db_mysql):
    response1 = client.patch(f'editor/{c.filename1}/{c.num_line1}/lock')
    response2 = client.patch(f'editor/{c.filename1}/{c.num_line1}/lock')

    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_304_NOT_MODIFIED


def test_unlock_line_succes(db_mysql):
    response1 = client.patch(f'editor/{c.filename1}/{c.num_line1}/lock')
    response2 = client.patch(f'editor/{c.filename1}/{c.num_line1}/unlock')
    response3 = client.get(f'editor/{c.filename1}/{c.num_line1}')
    data = json.loads(response3.content)

    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK
    assert response3.status_code == status.HTTP_200_OK
    assert not data['is_locked']


def test_unlock_line_NoFile_404(db_mysql):
    response = client.patch(f'editor/{c.filename2}/{c.num_line1}/unlock')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.filename2} in db'


def test_unlock_line_NoLine_404(db_mysql):
    response = client.patch(f'editor/{c.filename1}/{c.num_line_not_exists}/unlock')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert data['detail'] == f'no {c.num_line_not_exists} line in {c.filename1}'


def test_unlock_line_NoDateForUpdate_304(db_mysql):
    response = client.patch(f'editor/{c.filename1}/{c.num_line1}/unlock')
    assert response.status_code == status.HTTP_304_NOT_MODIFIED


def test_delete_line_succes(db_mysql):
    response1 = client.patch(f'editor/{c.filename1}/{c.num_line1}/lock')
    response2 = client.delete(f'editor/{c.filename1}/{c.num_line1}')

    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK


def test_delete_line_NoFilenameInDb_404(db_mysql):
    response = client.delete(f'editor/{c.filename2}/{c.num_line1}')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_line_ErrorNumLine_404(db_mysql):
    response = client.delete(f'editor/{c.filename1}/{c.num_line_not_exists}')
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_file_succes(db_mysql):
    response = client.delete(f'editor/{c.filename1}')
    assert response.status_code == status.HTTP_200_OK


def test_delete_file_NoFilenameInDb_404(db_mysql):
    response = client.delete(f'editor/{c.filename2}')
    assert response.status_code == status.HTTP_404_NOT_FOUND