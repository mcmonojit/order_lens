from pathlib import Path

from resources import config
from src.utils.s3.s3_client import S3ClientManager

# use a raw string 'r' so backslashes don't cause errors
# DATA_DIR = Path(r"E:\PyCharmProjects\order_lens\data")
DATA_DIR = Path(config.local_data_directory)

s3_client_provider = S3ClientManager()
s3_client = s3_client_provider.get_client()
bucket_name = config.S3_BUCKET_NAME

for csv_file in DATA_DIR.glob("*.csv"):
    s3_base_path = config.S3_BASE_PATH
    folder_name = csv_file.stem  #filename without .csv extension
    file_name = csv_file.name  #full filename including extension

    s3_key = f"{s3_base_path}/{folder_name}/{file_name}"

    s3_client.upload_file(
        Filename = str(csv_file),
        Bucket = bucket_name,
        Key = s3_key
    )

    #replace with logger later
    print(f"{file_name} upload completed...")

print(f"All files upload")