import os
import subprocess
from mimetypes import guess_type

from apps.core.bot.messages.messages import Messages
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import \
    drive_account_auth_with_oauth2client
from apps.MyBot import bot_send_message
from config.config import WRITE_DATA_ON_GOOGLE_DRIVE
from loader import logger

INSTALL_REQUIRES = ['google-api-core',
                    'google-api-python-client',
                    'google-auth-httplib2',
                    'google-auth-oauthlib',
                    'googleapis-common-protos',
                    'httplib2',
                    ]
MIME_TYPE_TEXT = "text/plain"
DESCRIPTION = "Uploaded Successfully"


def prepare_venv():
    """ Принудительное обновление / создание / подготовка виртуального окружения и venv с помощью subprocess.call
        установка зависимостей из requirements.txt
    """
    app_venv_name = "venv"

    if not os.path.exists(app_venv_name):
        os.makedirs(f"{app_venv_name}")
    # upgrade pip
    subprocess.call(['pip', 'install', '--upgrade'])
    # update requirements.txt and upgrade venv
    subprocess.call(['pip', 'install', '--upgrade'] + INSTALL_REQUIRES)


try:
    from googleapiclient.http import MediaFileUpload
except Exception as err:
    logger.error(f"*** googleapiclient error {err} ***")
    prepare_venv()


async def upload_file_on_gdrave(*, chat_id: str, drive_service: object, parent: str = None,
                                file_path: str = None, notify_user=True) -> str:
    """Авторизация (опционально), проверка пути и наличия файла, проверка типа файла.

    Загрузка (создание) файла на Google Drive. drive_service.files().create()

    Возвращает id загруженного файла в случаи успеха

    :param notify_user: оповещение пользователя
    :param file_path: путь к файлу
    :param parent: родительская папка в которую будет загружен файл на Google Drive
    :param chat_id: id чата для направления ответа ботом MyBot
    :param drive_service: объект авторизации
    :return: uploaded_file_id
    """

    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return 'error'

    if not drive_service: drive_service = await drive_account_auth_with_oauth2client()

    if not file_path:
        if notify_user:
            await bot_send_message(chat_id=chat_id,
                                   text=Messages.Error.upload_on_web,
                                   disable_notification=True)
        logger.error(f"File {file_path} not found")
        return 'error'

    if not os.path.isfile(file_path):
        logger.error(f"File {file_path} not found")
        return 'error'

    mime_type = guess_type(file_path)[0]
    mime_type = mime_type if mime_type else MIME_TYPE_TEXT

    media_body = MediaFileUpload(file_path,
                                 mimetype=mime_type,
                                 chunksize=150 * 1024 * 1024,
                                 resumable=True
                                 )

    file_name = os.path.basename(file_path)

    filesize = await humanbytes(os.path.getsize(file_path))

    body = {
        "name": file_name,
        "description": DESCRIPTION,
        "mimeType": mime_type,
    }

    if parent:
        body["parents"] = parent
    try:
        uploaded_file = drive_service.files().create(body=body,
                                                     media_body=media_body,
                                                     fields='id',
                                                     supportsTeamDrives=True).execute()
        uploaded_file_id = uploaded_file.get('id')

        logger.info(f'**Uploading...**\n**Filename:** ```{file_name}```\n**Size:** ```{filesize}```')
        if notify_user:
            await bot_send_message(
                chat_id=chat_id,
                text=f'**Uploading...**  **Filename:** ```{file_name}```\n**Size:** ```{filesize}```',
                disable_notification=True
            )

        return uploaded_file_id

    except Exception as uploaded_err:
        if notify_user:
            await bot_send_message(chat_id=chat_id, text=f'**ERROR:** ```{uploaded_err}```', disable_notification=True)
        return 'error'


# async def upload_photo_file_on_gdrave(*, chat_id: str, drive_service: object, parent: str = None,
#                                       file_path: str = None) -> str:
#     """Авторизация (опционально), проверка пути и наличия файла, проверка типа файла.
#
#     Загрузка (создание) файла на Google Drive. drive_service.files().create()
#
#     Возвращает id загруженного файла в случаи успеха
#
#     :param file_path: путь к файлу
#     :param parent: родительская папка в которую будет загружен файл на Google Drive
#     :param chat_id: id чата для направления ответа ботом MyBot
#     :param drive_service: объект авторизации
#     :return: uploaded_file_id
#     """
#     if not file_path:
#             if notify_user:
#         await MyBot.dp.bot.send_message(chat_id, Messages.Error.upload_on_web,
#                                         disable_notification=True)
#
#     if not os.path.isfile(file_path):
#         logger.info(f"File {file_path} not found")
#         return ''
#
#     mime_type = guess_type(file_path)[0]
#     mime_type = mime_type if mime_type else MIME_TYPE_TEXT
#
#     media_body = MediaFileUpload(file_path,
#                                  mimetype=mime_type,
#                                  chunksize=150 * 1024 * 1024,
#                                  resumable=True
#                                  )
#
#     file_name = os.path.basename(file_path)
#
#     filesize = await humanbytes(os.path.getsize(file_path))
#
#     body = {
#         "name": file_name,
#         "description": DESCRIPTION,
#         "mimeType": mime_type,
#     }
#
#     if parent:
#         body["parents"] = parent
#     try:
#         uploaded_file = drive_service.files().create(body=body,
#                                                      media_body=media_body,
#                                                      fields='id',
#                                                      supportsTeamDrives=True).execute()
#         file_id = uploaded_file.get('id')
#
#         logger.info(f'**Uploading...**\n**Filename:** ```{file_name}```\n**Size:** ```{filesize}```')
#         if notify_user:
#               await MyBot.dp.bot.send_message(chat_id,
#                                         f'**Uploading...**  **Filename:** ```{file_name}```\n**Size:** ```{filesize}```',
#                                         disable_notification=True)
#         return file_id
#
#     except Exception as uploaded_err:
#           if notify_user:
#               await MyBot.dp.bot.send_message(chat_id, f'**ERROR:** ```{uploaded_err}```', disable_notification=True)
#         return 'error'
#
#
# async def upload_report_file_on_gdrave(*, chat_id: str, drive_service: object, parent: str = None,
#                                        file_path: str = None) -> str:
#     """Авторизация (опционально), проверка пути и наличия файла, проверка типа файла.
#
#     Загрузка (создание) файла на Google Drive. drive_service.files().create()
#
#     Возвращает id загруженного файла в случаи успеха
#
#     :param file_path: путь к файлу
#     :param parent: родительская папка в которую будет загружен файл на Google Drive
#     :param chat_id: id чата для направления ответа ботом MyBot
#     :param drive_service: объект авторизации
#     :return: uploaded_file_id
#     """
#     if not file_path:
#         await MyBot.dp.bot.send_message(chat_id=chat_id,
#                                         text=Messages.Error.upload_on_web,
#                                         disable_notification=True)
#
#     if not os.path.isfile(file_path):
#         logger.info(f"File {file_path} not found")
#         return ''
#
#     mime_type = guess_type(file_path)[0]
#     mime_type = mime_type if mime_type else MIME_TYPE_TEXT
#
#     media_body = MediaFileUpload(file_path,
#                                  mimetype=mime_type,
#                                  chunksize=150 * 1024 * 1024,
#                                  resumable=True
#                                  )
#
#     file_name = os.path.basename(file_path)
#
#     body = {
#         "name": file_name,
#         "description": DESCRIPTION,
#         "mimeType": mime_type,
#     }
#
#     if parent:
#         body["parents"] = parent
#     try:
#         uploaded_file = drive_service.files().create(body=body,
#                                                      media_body=media_body,
#                                                      fields='id',
#                                                      supportsTeamDrives=True).execute()
#         file_id = uploaded_file.get('id')
#
#         return file_id
#
#     except Exception as uploaded_err:
#         await MyBot.dp.bot.send_message(chat_id=chat_id, text=f'**ERROR:** ```{uploaded_err}```',
#                                         disable_notification=True)
#         return 'error'


async def humanbytes(f_size: int) -> str:
    """Представление размера файла в читабельном формате

    Example:
        100000000B -> 1000 КB

    :type f_size: int
    :param f_size: размер в байтах
    :return: читабельное представления размера файла
    """
    if not f_size:
        return ""
    power = 2 ** 10
    number = 0
    dict_power_n = {0: " ",
                    1: "K",
                    2: "M",
                    3: "G",
                    4: "T",
                    5: "P"
                    }
    while f_size > power:
        f_size /= power
        number += 1
    return str(round(f_size, 2)) + " " + dict_power_n[number] + 'B'
