import os
import boto3

from fastapi.responses import FileResponse


class S3Client():
    
    def __init__(self) -> None:
        self.client_s3 = boto3.client('s3',
                                      aws_access_key_id= os.environ['ACCESS_KEY'],
                                      aws_secret_access_key= os.environ['ACCESS_SECRET'],
                                      )
        self.bucket_name = os.environ['BUCKET_NAME']

    def upload_file(self, file, key:str):
        self.client_s3.upload_fileobj(Bucket=self.bucket_name,
                                      Fileobj=file.file,
                                      Key=f"{key}.{self.extension_file(file)}")
        return {'key': key,
                'file_name': file.filename,
                'extension': self.extension_file(file)}
        
    def extension_file(self, file):
        return file.filename.split('.')[-1]
    
    def path_to_download(self, key:str):
        return os.path.join(
            os.path.join(os.getcwd(), 'download'),
            key
        )

    def download_file(self, key:str):
        self.client_s3.download_file(Bucket=self.bucket_name,
                                     Key=key,
                                     Filename=self.path_to_download(key)
                                    )
        return FileResponse(self.path_to_download(key))