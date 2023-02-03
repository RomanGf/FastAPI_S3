import os
import uvicorn
import boto3

from boto.s3.key import Key
from botocore.exceptions import ClientError

from typing import List

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

# move to environment variables
# create class S3 with 2 method upload and download

ACCESS_KEY = "AKIAR3OQPIJMJ2G6BINW"
ACCESS_SECRET = "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"
BUCKET_NAME = "rrstoragebucket"

app = FastAPI()
# create class document manager with 2 method upload and download
 
client_s3 = boto3.client(
    's3',
    aws_access_key_id= ACCESS_KEY,
    aws_secret_access_key= ACCESS_SECRET
)


@app.get('/api/file/{key}')
async def get_file(key:str):
    path_to_download = os.path.join(os.getcwd(), 'download')
    client_s3.download_file(BUCKET_NAME, 
                        Key=key, 
                        Filename=os.path.join(path_to_download, key) 
                        )
    return FileResponse(os.path.join(path_to_download, key))


@app.post('/api/file')
async def upload_file(key:str, file:UploadFile = File(...)):
    extension_file = file.filename.split('.')[-1]
    try:
        print(f'Uploading file {file}...')
        client_s3.upload_fileobj(
            file.file,
            BUCKET_NAME,
            f'{key}.{extension_file}',
        )
    except ClientError as e:
        print("Credential is incorrect")
        print(e)
    except Exception as e:
        print(e)
    return {'key': key,
            'file_name': file.filename,
            'extension': extension_file}


@app.put('/api/file/{key}')
async def update_file(key:str, file:UploadFile = File(...)):
    client_s3.put_object(Bucket=BUCKET_NAME,
                         Key=key, 
                         Body=file.file, 
                         ContentType='image/jpg', 
                        )
    return {"message": 'file updated'}

if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)