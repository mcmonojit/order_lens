# S3 CSV Upload Script — Step-by-Step Guide

## What You're Building

A script that:
1. Reads every `.csv` from `data/`
2. For each file (e.g. `orders.csv`), creates a folder `orders/` inside your S3 path
3. Uploads the file as `orders/orders.csv`

---

## Step 1 — Install the AWS SDK

```bash
pip install boto3
```

---

## Step 2 — Create `config.py`

Create `config.py` in the project root with these variables:

```python
BUCKET_NAME = "your-bucket-name"
S3_BASE_PATH = "your/prefix/path"   # e.g. "raw/order_lens" — no leading/trailing slash
```

---

## Step 3 — Set Up AWS Credentials

Boto3 picks up credentials automatically. Choose one method:

**Option A — AWS CLI (recommended)**
```bash
aws configure
# Enter: Access Key ID, Secret Access Key, region
```

**Option B — Environment variables**
```bash
set AWS_ACCESS_KEY_ID=...
set AWS_SECRET_ACCESS_KEY=...
set AWS_DEFAULT_REGION=ap-south-1
```

---

## Step 4 — Create `upload_to_s3.py`

Build the script yourself using these building blocks:

### 4a. Imports you'll need
```python
import boto3
import os
from pathlib import Path
from config import BUCKET_NAME, S3_BASE_PATH
```

### 4b. Point to the data directory
```python
DATA_DIR = Path("data")
```

### 4c. Create a boto3 S3 client
```python
s3 = boto3.client("s3")
```

### 4d. Loop over CSV files

`DATA_DIR.glob("*.csv")` returns a generator of `Path` objects — one per `.csv` file found in `data/`. Each `csv_file` is a `Path` you can use directly in the next two steps.

```python
for csv_file in DATA_DIR.glob("*.csv"):
    # csv_file is a Path object, e.g. Path("data/orders.csv")
    # steps 4e and 4f go here, indented inside this loop
```

> **Why not `os.listdir`?**  
> `os.listdir("data")` returns plain strings (e.g. `"orders.csv"`) with no path prefix. You would then need to filter for `.csv` manually and rebuild the full path:
> ```python
> for name in os.listdir("data"):
>     if not name.endswith(".csv"):
>         continue
>     csv_file = Path("data") / name   # re-construct path manually
> ```
> Both work, but `Path.glob` does all of this in one line and is preferred.

### 4e. Build the S3 key for each file

The target S3 key for `orders.csv` is:
```
your/prefix/path/orders/orders.csv
```

Break this down:
- `S3_BASE_PATH` → `"your/prefix/path"` (from config)
- `csv_file.stem` → `"orders"` (filename without `.csv` extension — this becomes the folder name)
- `csv_file.name` → `"orders.csv"` (full filename including extension)

```python
folder_name = csv_file.stem                          # "orders"
s3_key = f"{S3_BASE_PATH}/{folder_name}/{csv_file.name}"
# result: "your/prefix/path/orders/orders.csv"
```

### 4f. Upload the file

`s3.upload_file` takes three things: the **local file path as a string**, the **bucket name**, and the **S3 key** you built in 4e.

```python
s3.upload_file(
    Filename=str(csv_file),   # local path: "data/orders.csv"
    Bucket=BUCKET_NAME,
    Key=s3_key                # S3 key: "your/prefix/path/orders/orders.csv"
)
```

`csv_file` is a `Path` object, so wrap it with `str()` — `upload_file` expects a plain string for `Filename`.

### 4g. Print progress
After each upload, print the file name and the S3 key so you can verify.

---

## Step 5 — Run and Verify

```bash
python upload_to_s3.py
```

Check your S3 bucket in the AWS console. You should see:

```
your/prefix/path/
  orders/
    orders.csv
  users/
    users.csv
  ...
```

---

## Files in `data/` That Will Be Uploaded

| File | S3 Folder |
|---|---|
| orders.csv | orders/ |
| users.csv | users/ |
| restaurants.csv | restaurants/ |
| menu.csv | menu/ |
| order_items.csv | order_items/ |
| reviews.csv | reviews/ |
| food.csv | food/ |

---

## Common Errors

| Error | Fix |
|---|---|
| `NoCredentialsError` | Run `aws configure` or set env vars |
| `NoSuchBucket` | Check `BUCKET_NAME` in config.py |
| `ModuleNotFoundError: boto3` | Run `pip install boto3` |
