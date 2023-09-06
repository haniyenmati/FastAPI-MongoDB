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
