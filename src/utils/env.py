import dotenv
import os
from enum import Enum


def load_env(field: str) -> dict:
    field = field.upper()  # make sure its upper case

    if f'{field}_ENV' not in os.environ:
        dotenv.load_dotenv()
    return {
        key: os.environ[key]
        for key in os.environ
        if key.startswith(field)
    }


class EnvFields(str, Enum):
    Web = 'WEB'
    DB = 'DB'
    Security = 'SEC'
    File = 'FILE'
