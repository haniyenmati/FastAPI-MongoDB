import uvicorn
from utils import env


if __name__ == "__main__":
    env_args = env.load_env(field=env.EnvFields.Web)
    uvicorn.run(
        app=env_args.get("WEB_APP"),
        host=env_args.get("WEB_HOST"),
        port=int(env_args.get("WEB_PORT")),
        reload=True
    )
