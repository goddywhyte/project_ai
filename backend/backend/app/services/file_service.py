import os
from uuid import uuid4

UPLOAD_DIR = "uploads"


def save_file(file, subfolder: str):
    os.makedirs(f"{UPLOAD_DIR}/{subfolder}", exist_ok=True)

    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"

    file_path = f"{UPLOAD_DIR}/{subfolder}/{filename}"

    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path