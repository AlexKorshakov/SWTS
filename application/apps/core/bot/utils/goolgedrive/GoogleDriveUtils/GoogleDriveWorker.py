from __future__ import print_function

import os
import pickle
import subprocess
from pathlib import Path
from typing import Coroutine

from config.config import SERVICE_ACCOUNT_FILE, WRITE_DATA_ON_GOOGLE_DRIVE
from loader import logger

INSTALL_REQUIRES: list = ['google-api-core',
                          'google-api-python-client',
                          'google-auth-httplib2',
                          'google-auth-oauthlib',
                          'googleapis-common-protos',
                          'httplib2',
                          ]


def prepare_venv():
    """ Принудительное обновление / создание / подготовка виртуального окружения и venv с помощью subprocess.call
        установка зависимостей из requirements.txt
    """
    app_venv_name = "venv"

    if not os.path.exists(app_venv_name):
        os.makedirs(f"{app_venv_name}")
    # upgrade pip
    subprocess.call(['pip', 'install', '--upgrade', 'pip'])
    # update requirements.txt and upgrade venv
    subprocess.call(['pip', 'install', '--upgrade'] + INSTALL_REQUIRES)


try:
    from googleapiclient.discovery import build
    import httplib2
    from google.oauth2 import service_account
except Exception as err:
    logger.error(f"*** google api client error {err} ***")
    prepare_venv()

# logger.info("V 0.043 master GoogleDriveWorker")

SCOPE_DRIVE: str = "https://www.googleapis.com/auth/drive"

SCOPE_DRIVE_APPDATA: str = "https://www.googleapis.com/auth/drive.appdata"
# Просмотр и управление файлами и папками Google Drive, которые вы открыли или создали с помощью этого приложения
SCOPE_DRIVE_FILE = "https://www.googleapis.com/auth/drive.file"

SCOPES: list = [SCOPE_DRIVE,
                SCOPE_DRIVE_APPDATA,
                SCOPE_DRIVE_FILE
                ]

PICKLE_PATH: str = '\\token.pickle'
WORK_PATH = str(Path(__file__).resolve().parent)


async def drive_account_credentials() -> Coroutine:
    """Авторизация на Google
    """

    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return

    credentials = None
    # Файл token.pickle хранит токены доступа и обновления пользователя
    # и создается автоматически при первом завершении процесса авторизации.
    if os.path.exists(WORK_PATH):
        logger.info(f'{WORK_PATH + PICKLE_PATH}')
        with open(WORK_PATH + PICKLE_PATH, 'rb') as token:
            credentials = pickle.load(token)

        if not credentials:
            # Читаем ключи из файла
            credentials = service_account.Credentials.from_service_account_file(
                filename=SERVICE_ACCOUNT_FILE,
                scopes=SCOPES)

            with open(WORK_PATH + PICKLE_PATH, 'wb') as token:
                pickle.dump(credentials, token)

        # Авторизуемся в системе
        http_auth = credentials.authorize(httplib2.Http())

        try:
            # Выбираем работу с Google Drive и 3 версию API
            google_drive_service = build('drive', 'v3', http=http_auth)
            logger.info("**Already authorized your Google Drive Account.**")
            return google_drive_service

        except Exception as authorized_err:
            logger.error(f"авторизация успешно провалена! : {repr(authorized_err)} ")


async def drive_account_auth_with_oauth2client() -> object:
    """Авторизация на GoogleDisc и получение объекта авторизации
    """
    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return

    google_drive_service = await drive_account_credentials()
    return google_drive_service


async def move_file(service: object, *, file_id: str, add_parents: str, remove_parents: str) -> None:
    """Перемещение файла/папки из одной папки в другую

    :param service: объект авторизации
    :param file_id: id файла / папки которую будет перемещаться
    :param add_parents: id  каталога в который перемещается файл / папка
    :param remove_parents: id  каталога из которого перемещается файл / папка
    :rtype: object
    """
    try:
        service.files().update(fileId=file_id, addParents=add_parents, removeParents=remove_parents).execute()
    except Exception as update_err:
        logger.error(f"move_folder err {file_id} to move in add_parents \n: {repr(update_err)}")
