from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.set_user_violation_data_on_google_drave import \
    JSON_FOLDER_NAME, PHOTO_FOLDER_NAME, REPORT_FOLDER_NAME
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import \
    drive_account_auth_with_oauth2client
from apps.core.utils.goolgedrive_processor.googledrive_worker import ROOT_REPORT_FOLDER_NAME, get_report_folder_id, \
    get_photo_folder_id, get_json_folder_id, get_root_folder_id, get_user_folder_id
from config.config import WRITE_DATA_ON_GOOGLE_DRIVE

from loader import logger


async def get_folders_ids_from_google_drive(user: str, drive_service: object = None):
    """ Получение id основных папок для chat_id для загрузки в облачный репозиторий

        Подготовка данных к загрузке на Google Drive

        Дополнение violation_data

        :param user: id пользователя
        :param drive_service: объект авторизации

        :return: {'user_folder_id', 'json_folder_id', 'photo_folder_id', 'report_folder_id',} or {}
        """

    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return {}

    if not drive_service: drive_service = await drive_account_auth_with_oauth2client()

    if not drive_service:
        logger.error(f"drive_service is empty {drive_service = }")
        return {}

    root_folder_id = await get_root_folder_id(drive_service=drive_service,
                                              root_folder_name=ROOT_REPORT_FOLDER_NAME)
    if not root_folder_id:
        return {}

    user_folder_id = await get_user_folder_id(drive_service=drive_service,
                                              root_folder_name=str(user),
                                              parent_id=root_folder_id, )

    json_folder_id = await get_json_folder_id(drive_service=drive_service,
                                              json_folder_name=JSON_FOLDER_NAME,
                                              parent_id=user_folder_id,
                                              root_json_folder_id=user_folder_id)

    photo_folder_id = await get_photo_folder_id(drive_service=drive_service,
                                                photo_folder_name=PHOTO_FOLDER_NAME,
                                                parent_id=user_folder_id,
                                                root_photo_folder_id=user_folder_id)

    report_folder_id = await get_report_folder_id(drive_service=drive_service,
                                                  report_folder_name=REPORT_FOLDER_NAME,
                                                  parent_id=user_folder_id,
                                                  root_report_folder_id=user_folder_id)

    if not json_folder_id:
        return {}

    return {
        'json_folder_id': json_folder_id,
        'photo_folder_id': photo_folder_id,
        'report_folder_id': report_folder_id,
        'user_folder_id': user_folder_id
    }
