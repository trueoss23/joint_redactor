from fastapi.testclient import TestClient
from fastapi import status

import json

from main import app
from common.exceptions import NoFilenameInDb, FilenameAlreadyExists, ErrorNumLine
import constants as c

client = TestClient(app=app)


def test_read_file_succes(db_mem):
    response = client.get(f'/editor/{c.filename1}')
    data = json.loads(response.content)
    assert response.status_code == status.HTTP_200_OK
    # print('left', data[c.filename1], '\nrigth', c.lines1)
    print('dataaaa', data)
    print('c.file1', c.file1)
    assert dict(data) == dict(c.file1) 
