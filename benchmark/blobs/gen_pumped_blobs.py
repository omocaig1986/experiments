from shutil import copyfile
import os

BLOB_PATH = "."
BLOB_NAME = "family"
BLOB_EXTENSION = "jpg"


def gen(size):
    """Size in bytes"""
    original_file = f"{BLOB_PATH}/{BLOB_NAME}.{BLOB_EXTENSION}"
    original_size = os.path.getsize(original_file)
    print(original_size)

    new_file = f"{BLOB_PATH}/{BLOB_NAME}_{size}bytes.{BLOB_EXTENSION}"
    copyfile(original_file, new_file)
    print(new_file)

    bytes_to_write = size-original_size
    blob_file = open(new_file, "ab")
    for i in range(bytes_to_write):
        blob_file.write(b'0')
    blob_file.close()

gen(50000)  # 50kb
for i in range(1, 10):
    gen(i*100000)  # 100kb
