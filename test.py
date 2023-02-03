import os
import boto3
import moto
import pytest

from fastapi.testclient import TestClient
from tempfile import NamedTemporaryFile
from botocore.exceptions import ClientError

from .main import app

client = TestClient(app)



def test_get_file():
    response = client.get('/api/file/vanya.jpg')
    assert response.status_code == 200

def test_upload_file():
    test_file ='lol.txt'
    response = client.post('/api/files/lol.txt', json={'key':'tyktyk',
    'file':test_file})
    assert response.status_code == 404

