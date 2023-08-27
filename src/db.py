from mongoengine import connect, disconnect
from utils import env
    

def __get_db_uri(DB_ENGINE, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME):
    return f"{DB_ENGINE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def init():
    db_env = env.load_env(field=env.EnvFields.DB)
    db_env.pop("DB_ENV")

    URI = __get_db_uri(**db_env)

    return connect(host=URI)


def shutdown():
    disconnect()