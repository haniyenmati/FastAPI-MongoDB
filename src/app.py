import db
from fastapi import FastAPI
from utils import env, exceptions
from logging import Logger


def create_app(debug: bool = False) -> FastAPI:
    env_args = env.load_env(field=env.EnvFields.Web)
    app = FastAPI(
        title=env_args.get("WEB_APP_TITLE"),
        version=env_args.get("WEB_APP_VERSION"),
        debug=debug
    )
    register_views(app=app)
    return app


def register_views(app: FastAPI):
    from routes.auth import router as AuthRouter
    from routes.files import router as FilesRouter

    app.include_router(AuthRouter)
    app.include_router(FilesRouter)


app = create_app()
db_connection = None


app.add_exception_handler(exceptions.HTTPException,
                          exceptions.http_exception_handler)


@app.on_event("startup")
async def create_db_client():
    global db_connection
    print("DB is connecting ...")
    db_connection = db.init()
    print("DB connected!")


@app.on_event("shutdown")
async def shutdown_db_client():
    print("DB is disconnecting ...")
    db.shutdown()
    print("DB disconnected!")


@app.get('/')
async def startup():
    return {"status": "alive"}
