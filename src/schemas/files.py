from pydantic import BaseModel, UUID4
from typing import List
from datetime import datetime


class ImageOwner(BaseModel):
    username: str


class ImageUploadResponse(BaseModel):
    name: str
    owner: ImageOwner
    uuid: UUID4
    uploaded_at: datetime


class UserImagesResponse(BaseModel):
    images: List[ImageUploadResponse]
