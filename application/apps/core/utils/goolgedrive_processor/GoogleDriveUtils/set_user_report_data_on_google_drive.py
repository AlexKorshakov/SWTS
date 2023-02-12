from apps.core.utils.goolgedrive_processor.googledrive_worker import (
    ROOT_REPORT_FOLDER_NAME, get_report_folder_id, get_root_folder_id,
    get_user_folder_id)
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.folders_deleter import \
    del_by_name_old_data_google_drive
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import (
    drive_account_auth_with_oauth2client, move_file)
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.set_permissions import \
    get_user_permissions
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.upload_data_on_gdrive import \
    upload_file_on_gdrave
from config.config import WRITE_DATA_ON_GOOGLE_DRIVE
from loader import logger

REPORT_FOLDER_NAME = "reports"


async def set_user_report_data_on_google_drive(*, chat_id, full_report_path: str, drive_service: object = None):
    """ Загрузка данных на Google Drive

    :param chat_id:
    :param full_report_path: данные для записи
    :param drive_service: объект авторизации
    :return:
    """

    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return False

    if not drive_service:
        drive_service = await drive_account_auth_with_oauth2client()

    if not drive_service:
        logger.error(f"Error create drive_service!! return")
        return

    root_folder_id = await get_root_folder_id(
        drive_service=drive_service,
        root_folder_name=ROOT_REPORT_FOLDER_NAME
    )
    if not root_folder_id:
        return

    user_folder_id = await get_user_folder_id(
        drive_service=drive_service,
        root_folder_name=str(chat_id),
        parent_id=root_folder_id
    )

    report_folder_id = await get_report_folder_id(
        drive_service=drive_service,
        report_folder_name=REPORT_FOLDER_NAME,
        parent_id=user_folder_id
    )

    report_name = full_report_path.split('\\')[-1]
    await del_by_name_old_data_google_drive(
        chat_id=chat_id,
        drive_service=drive_service,
        parent=report_folder_id,
        name=report_name
    )

    report_file_id = await upload_file_on_gdrave(
        chat_id=chat_id,
        drive_service=drive_service,
        parent=report_folder_id,
        file_path=full_report_path
    )

    await get_user_permissions(
        drive_service=drive_service,
        file_id=report_file_id
    )

    await move_file(
        service=drive_service,
        file_id=report_file_id,
        add_parents=report_folder_id,
        remove_parents=root_folder_id
    )

    return True
