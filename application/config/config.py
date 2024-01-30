import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from environs import Env, EnvError

env = Env()
env.read_env()

# BASE_DIR = Path(__file__).resolve().parent
load_dotenv(Path(__file__).resolve().parent / "config" / ".env")

from loader import logger

logger.info('start config load')

try:
    BOT_TOKEN: str = env("BOT_TOKEN")
except EnvError as env_err:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error('You have forgot to set BOT_TOKEN')
        sys.exit(0)

WRITE_DATA_ON_GOOGLE_DRIVE = env.bool("WRITE_DATA_ON_GOOGLE_DRIVE", False)
ADMINS_ID: list = [373084462]
ADMIN_ID: str = env("ADMIN_ID")
ADMIN_EMAIL: str = env("ADMIN_EMAIL")
DEVELOPER_ID: int = env("DEVELOPER_ID")
DEVELOPER_EMAIL: str = env("DEVELOPER_EMAIL")

WRITE_DATA_ON_GOOGLE_DRIVE = env("WRITE_DATA_ON_GOOGLE_DRIVE")

BASE_DIR: Path = Path(__file__).parent.parent


dbs_main_folder: str = '!DataBase'
Udocan_DB_path: Path = Path(BASE_DIR.parent.parent, dbs_main_folder)
Udocan_HSE_user_base_storage: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'Udocan_HSE_user_base_storage.db')
Udocan_Trainings_DB: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'Udocan_Trainings_DB.db')
Udocan_Enable_Features_DB: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'UdocanEnableFeaturesDataBase.db')
Udocan_Catalog_Employee_DB: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'UdocanEmployeesDatabase.db')
Udocan_Access_DB: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'UdocanAccessDatabase.db')
Udocan_Catalog_DB: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, '!catalog')
Udocan_MSG_DB: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'UdocanMSGDataBase.db')
Udocan_Bagration_subcontractor_employee_DB: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'UdocanBagrationDataBase.db')
Udocan_main_data_base_dir: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'UdocanHSEViolationsDataBase.db')
Udocan_HSE_Violations_DB: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'UdocanHSEViolationsDataBase.db')
Udocan_media_path: Path = Path(BASE_DIR.parent.parent, '!media')
Udocan_HSE_media_path: Path = Path(BASE_DIR.parent.parent, '!media', 'HSE')

Udocan_LNA_path: Path = Path(BASE_DIR.parent.parent, '!media', 'LNA')

Udocan_HSE_Check_Lists: Path = Path(BASE_DIR.parent.parent, dbs_main_folder, 'UdocanHSECheckListsDataBase.db')

PRIVATE_KEY: str = env("PRIVATE_KEY")

SENDER: str = env("SENDER")
SENDER_ACCOUNT_GMAIL: str = env("SENDER_ACCOUNT_GMAIL")
SENDER_ACCOUNT_PASSWORD: str = env("SENDER_ACCOUNT_PASSWORD")

ROOT_REPORT_FOLDER_NAME: str = env("ROOT_REPORT_FOLDER_NAME")
ROOT_REPORT_FOLDER_ID: str = env("ROOT_REPORT_FOLDER_ID")

SKIP_UPDATES = env.bool("SKIP_UPDATES", False)
BOT_DELETE_MESSAGE = True
NUM_BUTTONS = env.int("NUM_BUTTONS", 6)
REPORT_NAME: str = "report_data___"
SEPARATOR = "___"

# Путь к файлу с данными сервисного аккаунта
SERVICE_ACCOUNT_FILE: str = '.\\apps\\core\\bot\\data\\service_account_myctng.json'

logger.info('end config load')
# Init config
if 'init' in sys.argv:
    logger.error(f'sys.argv: {sys.argv}')
    sys.exit(0)
