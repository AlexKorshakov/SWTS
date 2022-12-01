import os
import sys

from dotenv import load_dotenv
from environs import Env, EnvError
from pathlib import Path

from loader import logger

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / "config" / ".env")

try:
    BOT_TOKEN: str = env("BOT_TOKEN")
except EnvError as env_err:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error('You have forgot to set BOT_TOKEN')
        quit()

WRITE_DATA_ON_GOOGLE_DRIVE = env.bool("WRITE_DATA_ON_GOOGLE_DRIVE", False)
ADMINS_ID: str = env("ADMINS_ID")
ADMIN_ID: str = env("ADMIN_ID")
ADMIN_EMAIL: str = env("ADMIN_EMAIL")
DEVELOPER_ID: int = env("DEVELOPER_ID")
DEVELOPER_EMAIL: str = env("DEVELOPER_EMAIL")

PRIVATE_KEY: str = env("PRIVATE_KEY")

SENDER: str = env("SENDER")
SENDER_ACCOUNT_GMAIL: str = env("SENDER_ACCOUNT_GMAIL")
SENDER_ACCOUNT_PASSWORD: str = env("SENDER_ACCOUNT_PASSWORD")

ROOT_REPORT_FOLDER_NAME: str = env("ROOT_REPORT_FOLDER_NAME")
ROOT_REPORT_FOLDER_ID: str = env("ROOT_REPORT_FOLDER_ID")

SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
BOT_DELETE_MESSAGE = True

NUM_BUTTONS = env.int("NUM_BUTTONS", 5)

WORK_PATH = os.getcwd()

REPORT_NAME: str = "report_data___"

SEPARATOR = "___"

# Путь к файлу с данными сервисного аккаунта
SERVICE_ACCOUNT_FILE: str = '.\\apps\\core\\bot\\data\\service_account_myctng.json'

# Init config
if 'init' in sys.argv:
    logger.info(f'sys.argv: {sys.argv}')
    sys.exit(0)
