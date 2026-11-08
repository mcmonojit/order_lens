import os
import boto3
from dotenv import load_dotenv

class S3ClientManager:
    def __init__(self):
        load_dotenv()
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id = os.getenv("AWS_ACCESS_KEY"),
            aws_secret_access_key = os.getenv("AWS_SECRET_KEY"),
            region_name = os.getenv("AWS_S3_BUCKET_REGION")
        )

    def get_client(self):
        return self.s3_client