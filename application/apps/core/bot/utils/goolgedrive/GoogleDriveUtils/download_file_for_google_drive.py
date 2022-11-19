import io
import os
import subprocess

from loader import logger

from config.config import SEPARATOR, WRITE_DATA_ON_GOOGLE_DRIVE
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.get_folder_id import get_root_folder_id, get_user_folder_id, \
    get_json_folder_id, get_photo_folder_id
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.set_user_violation_data_on_google_drave import JSON_FOLDER_NAME, \
    PHOTO_FOLDER_NAME
from apps.core.bot.utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_NAME
from apps.core.bot.utils.secondary_functions.get_part_date import get_day_message, get_month_message

INSTALL_REQUIRES = ['google-api-core',
                    'google-api-python-client',
                    'google-auth-httplib2',
                    'google-auth-oauthlib',
                    'googleapis-common-protos',
                    # 'oauth2client',
                    'httplib2',
                    ]


def prepare_venv():
    """ принудительное обновление / создание / подготовка виртуального окружения и venv с помощью subprocess.call
        установка зацисимостей из requirements.txt
    """
    app_venv_name = "venv"

    if not os.path.exists(app_venv_name):
        os.makedirs(f"{app_venv_name}")
    # upgrade pip
    subprocess.call(['pip', 'install', '--upgrade'])
    # update requirements.txt and upgrade venv
    subprocess.call(['pip', 'install', '--upgrade'] + INSTALL_REQUIRES)


try:
    from googleapiclient.http import MediaIoBaseDownload
except Exception as err:
    logger.error(f"*** googleapiclient error {err} ***")
    prepare_venv()


async def upload_files_from_google_drive(chat_id, file_path, photo_path):
    """Загрузка файлов в облако Google Drive

    :param chat_id:
    :param file_path:
    :param photo_path:
    :return:
    """
    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return False

    drive_service = await drive_account_auth_with_oauth2client()

    if not drive_service:
        logger.info(f"🔒 **drive_service {drive_service} in Google Drive.**")
        return

    root_folder_id = await get_root_folder_id(drive_service,
                                              root_folder_name=ROOT_REPORT_FOLDER_NAME)
    if not root_folder_id:
        return

    user_folder_id = await get_user_folder_id(drive_service,
                                              root_folder_name=str(chat_id),
                                              parent_id=root_folder_id)

    json_folder_id = await get_json_folder_id(drive_service,
                                              json_folder_name=JSON_FOLDER_NAME,
                                              parent_id=user_folder_id)

    photo_folder_id = await get_photo_folder_id(drive_service,
                                                photo_folder_name=PHOTO_FOLDER_NAME,
                                                parent_id=user_folder_id)

    json_files = await get_files_by_folder_id(drive_service=drive_service, folder_id=json_folder_id)

    for file in json_files:
        current_date = file["name"].split(SEPARATOR)[1]
        if str(current_date.split(".")[0]) == await get_day_message() and \
                str(current_date.split(".")[1]) == await get_month_message():
            await upload_file(drive_service=drive_service, file_id=file["id"],
                              file_full_name=file_path + file["name"])

    photo_files = await get_files_by_folder_id(drive_service=drive_service, folder_id=photo_folder_id)

    for file in photo_files:
        current_date = file["name"].split(SEPARATOR)[1]
        if str(current_date.split(".")[0]) == await get_day_message() and \
                str(current_date.split(".")[1]) == await get_month_message():
            await upload_file(drive_service=drive_service, file_id=file["id"],
                              file_full_name=photo_path + file["name"])


async def get_files_by_folder_id(drive_service: object, folder_id: str):
    """Получение списка файлов по id родительской папки
    """
    page_token = None
    q = f"'{folder_id}' in parents and trashed=false"
    files = []
    while True:
        response = drive_service.files().list(supportsTeamDrives=True,
                                              includeTeamDriveItems=True,
                                              q=q,
                                              spaces='drive',
                                              pageSize=200,
                                              fields='nextPageToken, files(id, name, mimeType,size)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            files.append(file)
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
    return files


async def upload_file(drive_service: object, file_id: str, file_full_name: str, file_name: str = None):
    """Загрузка файла file_id из репозитория Google Drive и сохранение по пути file_full_name

    :param drive_service: объект авторизации,
    :param file_name: имя загружаемого файла
    :param file_id: id файла на Google Drive
    :param file_full_name: полный путь файла
    :return:
    """
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(file_full_name, mode='wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()

        if file_name:
            logger.info(f"Download %d%% file {file_name} {file_id}" % int(status.progress() * 100))
        else:
            logger.info(f"Download %d%% file {file_id}" % int(status.progress() * 100))
