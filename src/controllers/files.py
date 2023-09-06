from fastapi import UploadFile, HTTPException, status
from uuid import uuid4
from datetime import datetime
from models.files import Image
from models.auth import User
from utils.files import AllowedFileTypes, store_file, EXTENSIONS, zip_files
from utils.shortcuts import get_object_or_none
from utils import env


file_env = env.load_env(env.EnvFields.File)


async def upload_file_controller(uploaded: UploadFile, owner: User):
    if uploaded.content_type not in AllowedFileTypes.list():
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "supported formats are image/png & image/jpeg")

    uploaded_at = datetime.utcnow()
    file_uuid = uuid4()
    content = await uploaded.read()
    extension = EXTENSIONS.get(uploaded.content_type)
    filename = f"{file_uuid}{extension}"
    base_dir = file_env.get("FILE_DIR_PATH")

    path = store_file(base_dir=base_dir, filename=filename, content=content)

    _file = Image(name=uploaded.filename, uuid=file_uuid,
                  owner=owner, uploaded_at=uploaded_at, path=path)
    _file.save()

    return _file._data


async def download_file_controller(file_uuid: str, owner: User):
    img = await get_object_or_none(Image, uuid=file_uuid)

    if not img:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "invalid uuid")

    if img.owner.username != owner.username:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "access denied")

    return {"path": img.path, "filename": img.name}


async def get_owner_files_controller(owner: User):
    images = Image.objects(owner=owner)
    return {"images": images}


async def download_images_zip_controller(owner: User):
    images = Image.objects(owner=owner)

    path_list = [img.path for img in images]
    zip_io = zip_files(path_list)

    return zip_io.getvalue()
