# Code Review: S3 Upload Module

**Date:** 2026-11-09  
**Files reviewed:** `src/utils/s3/upload_to_s3.py`, `src/utils/s3/s3_client.py`, `resources/config.py`

---

## 1. Logic Problems in `upload_to_s3.py`

### Critical Bug — S3 client is never constructed

**File:** `src/utils/s3/s3_client.py`, line 6

The constructor is named `__ini__` instead of `__init__`. This means `load_dotenv()` and `boto3.client(...)` are **never called**. As a result, `self.s3_client` is never assigned, and calling `get_client()` will raise:

```
AttributeError: 'S3ClientManager' object has no attribute 's3_client'
```

**Fix:**

```python
# Before
def __ini__(self):

# After
def __init__(self):
```

---

### Minor — Leading slash in `S3_BASE_PATH`

**File:** `resources/config.py`, line 2

```python
S3_BASE_PATH = "/raw"  # wrong
S3_BASE_PATH = "raw"   # correct
```

S3 object keys must not start with `/`. Using `/raw` creates a phantom empty-string "folder" at the bucket root with a `raw` subfolder inside it, instead of placing objects directly under `raw/`.

**This has been fixed** in `config.py`.

---

### Minor — `s3_base_path` read inside the loop

**File:** `src/utils/s3/upload_to_s3.py`, line 15

`config.S3_BASE_PATH` is fetched on every iteration, but it is a constant. Move it outside the loop.

```python
# Before (inside loop)
for csv_file in DATA_DIR.glob("*.csv"):
    s3_base_path = config.S3_BASE_PATH
    ...

# After (outside loop)
s3_base_path = config.S3_BASE_PATH
for csv_file in DATA_DIR.glob("*.csv"):
    ...
```

---

### Minor — No `if __name__ == "__main__":` guard

**File:** `src/utils/s3/upload_to_s3.py`

All upload logic runs at module level. If anything ever imports from this file, uploads trigger immediately as a side effect.

```python
# Wrap everything after the top-level assignments:
if __name__ == "__main__":
    for csv_file in DATA_DIR.glob("*.csv"):
        ...
```

---

### Minor — Misleading final print statement

**File:** `src/utils/s3/upload_to_s3.py`, line 30

```python
print(f"All files upload")   # wrong: f-string with no interpolation, bad grammar

print("All files uploaded.") # correct
```

---

## 2. Bucket Name in `config.py` vs `.env`

**Short answer: the bucket name is safe in `config.py`. AWS credentials must stay in `.env`.**

| Value | Sensitivity | Right place |
|---|---|---|
| `AWS_ACCESS_KEY` / `AWS_SECRET_KEY` | **Secret** — grants API access | `.env` (gitignored) |
| `AWS_S3_BUCKET_REGION` | Low — but environment-specific | `.env` is reasonable |
| `S3_BUCKET_NAME` | **Not a secret** — it is a resource name, like a table name | `config.py` is fine |

The bucket name alone grants no access — an attacker still needs valid AWS credentials to do anything with it. Keeping it in `config.py` is a common, accepted pattern.

**When to move `S3_BUCKET_NAME` to `.env`:** if you later have multiple environments (dev/staging/prod) with different bucket names, it becomes an environment-specific config value and `.env` is the right place to vary it per environment.

The `load_dotenv()` call belongs in `s3_client.py` (or at app entrypoint), not in `upload_to_s3.py`. The current structure is already correct — `upload_to_s3.py` does not touch `.env` directly.

---

## 3. Pre-commit Security Check

### Fixed before commit

| Issue | File | Action taken |
|---|---|---|
| `.idea/` IDE directory untracked | `.gitignore` | Added `.idea/` to `.gitignore` |
| `venv/` untracked | `.gitignore` | Added `venv/` to `.gitignore` |
| Hardcoded Windows path in `config.py` | `resources/config.py` | Replaced with `os.getenv("LOCAL_DATA_DIRECTORY", "data")` |
| Leading `/` in `S3_BASE_PATH` | `resources/config.py` | Removed leading slash |

### Clear to commit

- `.env` is gitignored — credentials are safe.
- `docs/create_access_secret_keys.txt` contains no real keys, only a setup guide.
- `S3_BUCKET_NAME` in `config.py` is not a secret — safe to commit.
- No actual AWS keys found anywhere in tracked files.

---

## Action Items

| Priority | File | Task |
|---|---|---|
| **Critical** | `src/utils/s3/s3_client.py:6` | Rename `__ini__` to `__init__` |
| **High** | `.env` | Add `LOCAL_DATA_DIRECTORY=E:\PyCharmProjects\order_lens\data` |
| Low | `src/utils/s3/upload_to_s3.py:15` | Move `s3_base_path` assignment outside the loop |
| Low | `src/utils/s3/upload_to_s3.py` | Add `if __name__ == "__main__":` guard |
| Low | `src/utils/s3/upload_to_s3.py:30` | Fix final print string |
