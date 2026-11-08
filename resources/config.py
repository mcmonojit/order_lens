import os
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_NAME = "orderlens-dev-ap-south-2-datalake"
S3_BASE_PATH = "raw"

local_data_directory = os.getenv("LOCAL_DATA_DIRECTORY", "data")