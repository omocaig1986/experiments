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


gen(500000) # 500kb
gen(1000000) # 1mb
gen(5000000) # 5mb
gen(8000000) # 8mb
gen(10000000) # 10mb
gen(13000000) # 10mb
gen(15000000) # 10mb
gen(20000000) # 20mb


