import os
import sys

from dotenv import load_dotenv
from environs import Env, EnvError
from pathlib import Path

env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / "config" / ".env")

try:
    BOT_TOKEN: str = env("BOT_TOKEN")
except EnvError as env_err:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        print('You have forgot to set BOT_TOKEN')
        quit()

from loader import logger

WRITE_DATA_ON_GOOGLE_DRIVE = env.bool("WRITE_DATA_ON_GOOGLE_DRIVE", False)
ADMINS_ID: list = [373084462]
ADMIN_ID: str = env("ADMIN_ID")
ADMIN_EMAIL: str = env("ADMIN_EMAIL")
DEVELOPER_ID: int = env("DEVELOPER_ID")
DEVELOPER_EMAIL: str = env("DEVELOPER_EMAIL")

DATA_BASE_DIR: str = env("DATA_BASE_DIR")
MEDIA_DIR: str = env("MEDIA_DIR")
MAIN_DIR: str = env('MAIN_DIR')

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
