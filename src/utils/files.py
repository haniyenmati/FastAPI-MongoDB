import os
import zipfile
from io import BytesIO
from enum import Enum


EXTENSIONS = {
    "image/png": ".png",
    "image/jpeg": ".jpeg",
    "image/jpg": ".jpg"
}


class AllowedFileTypes(str, Enum):
    PNG = "image/png"
    JPEG = "image/jpeg"
    JPG = "image/jpg"

    @classmethod
    def list(cls):
        return [cls.PNG, cls.JPEG]


def store_file(base_dir: str, filename: str, content):
    path = f'{base_dir}/{filename}'

    with open(path, 'wb') as f:
        f.write(content)

    return path


def zip_files(path_list: list):
    zip_io = BytesIO()

    with zipfile.ZipFile(zip_io, mode='w', compression=zipfile.ZIP_DEFLATED) as temp_zip:
        for path in path_list:
            fdir, fname = os.path.split(path)
            zip_path = os.path.join("archive", fname)
            temp_zip.write(path, zip_path)

    return zip_io
