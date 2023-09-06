from fastapi import APIRouter, Depends, status, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
from typing import Annotated
from models.auth import User
from controllers.files import (
    upload_file_controller,
    download_file_controller,
    download_images_zip_controller
)
from controllers.auth import get_current_user
from schemas.files import ImageUploadResponse, UserImagesResponse


router = APIRouter(
    prefix="/files",
    tags=["FILES"],
    dependencies=None
)


@router.put("/", response_model=ImageUploadResponse)
async def upload_file(user: Annotated[User, Depends(get_current_user)], uploaded: UploadFile = File(...)):
    res = await upload_file_controller(uploaded=uploaded, owner=user)
    return res


@router.get("/")
async def download_file(user: Annotated[User, Depends(get_current_user)], file_uuid: str):
    res = await download_file_controller(file_uuid=file_uuid, owner=user)
    return FileResponse(path=res.get("path"), filename=res.get("filename"))


@router.get("/images")
async def download_images_zip(user: Annotated[User, Depends(get_current_user)]):
    zip_io = await download_images_zip_controller(owner=user)
    return StreamingResponse(
        iter([zip_io]),
        media_type="application/x-zip-compressed",
        headers={
            "Content-Disposition": f"attachment; filename={user.username}_images.zip"}
    )
