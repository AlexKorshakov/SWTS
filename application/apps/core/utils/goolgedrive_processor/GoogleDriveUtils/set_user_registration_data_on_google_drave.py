from config.config import WRITE_DATA_ON_GOOGLE_DRIVE
from loader import logger

from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client, \
    move_file
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.set_permissions import get_user_permissions
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.folders_deleter import del_by_name_old_data_google_drive
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.upload_data_on_gdrive import upload_file_on_gdrave
from apps.core.utils.goolgedrive_processor.googledrive_worker import ROOT_REPORT_FOLDER_NAME, get_root_folder_id, \
    get_user_folder_id
from apps.core.utils.json_worker.writer_json_file import write_user_registration_data_on_json_on_local_storage


async def write_user_registration_data_on_google_drive(*, chat_id, user_data):
    """ Загрузка данных на Google Drive
    :param chat_id:
    :param user_data: данные для записи
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

    folder_id = await get_user_folder_id(drive_service,
                                         root_folder_name=str(chat_id),
                                         parent_id=root_folder_id)
    user_data["parent_id"] = folder_id

    await write_user_registration_data_on_json_on_local_storage(user_data=user_data)

    await del_by_name_old_data_google_drive(chat_id=chat_id,
                                            drive_service=drive_service,
                                            parent=user_data["parent_id"])

    registration_file_id = await upload_file_on_gdrave(chat_id=chat_id,
                                                       drive_service=drive_service,
                                                       file_path=user_data["reg_json_full_name"])

    await get_user_permissions(drive_service=drive_service,
                               file_id=registration_file_id)

    await move_file(service=drive_service,
                    file_id=registration_file_id,
                    add_parents=folder_id,
                    remove_parents=root_folder_id)

    return True
