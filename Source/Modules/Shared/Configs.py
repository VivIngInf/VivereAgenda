import os
from dotenv import load_dotenv, find_dotenv

token: str = ""
host: str = ""
isTesting: str = ""


def LoadConfigs() -> None:
    """Load configs from env file"""

    load_dotenv(find_dotenv())

    global token, host, isTesting

    token = os.environ.get("BOT_TOKEN")
    host = os.environ.get("DB_HOST")
    isTesting = os.environ.get("IS_TESTING")

    return None


def get_token() -> str: return token


def get_db_host() -> str: return host


def get_is_testing() -> str: return isTesting
