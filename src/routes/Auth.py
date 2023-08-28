from fastapi import APIRouter
from controllers.Auth import register_user


router = APIRouter(
    prefix="/auth",
    tags=["AUTH"],
    dependencies=None
)


# TODO better schema for req and res
@router.post("/register")
async def register(username: str, password: str):
    res = await register_user(username, password)
    return {"data": res}
