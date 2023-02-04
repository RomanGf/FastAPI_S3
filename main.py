import uvicorn

from s3client import S3Client
from dotenv import load_dotenv
from botocore.exceptions import ClientError
from fastapi import FastAPI, UploadFile, File


load_dotenv()

app = FastAPI()

        
@app.get('/api/file/{key}')
async def get_file(key:str):
   return S3Client().download_file(key)


@app.post('/api/file')
async def upload_file(key:str, file:UploadFile = File(...)):
    try:
        return S3Client().upload_file(file, key)        
    except ClientError as e:
        print("Credential is incorrect")
        print(e)
    except Exception as e:
        print(e)



if __name__ == '__main__':
    uvicorn.run(app='main:app', reload=True)