from fastapi import APIRouter
from controllers.Auth import register_controller, login_controller


router = APIRouter(
    prefix="/auth",
    tags=["AUTH"],
    dependencies=None
)


# TODO better schema for req and res
@router.post("/register")
async def register(username: str, password: str):
    res = await register_controller(username, password)
    return {"data": res}


@router.post("/login")
async def login(username: str, password: str):
    res = await login_controller(username, password)
    return {"data": res}
