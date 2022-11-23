from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client, \
    move_file
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.folders_deleter import del_by_name_old_data_google_drive
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.get_folder_id import get_root_folder_id, get_user_folder_id, \
    get_json_folder_id
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.set_permissions import get_user_permissions
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.upload_data_on_gdrive import upload_file_on_gdrave
from apps.core.utils.goolgedrive_processor.googledrive_worker import ROOT_REPORT_FOLDER_NAME
from apps.core.utils.json_worker.writer_json_file import write_json_violation_user_file
from config.config import REPORT_NAME, WRITE_DATA_ON_GOOGLE_DRIVE
from loader import logger

JSON_FOLDER_NAME = "violation_json"
PHOTO_FOLDER_NAME = "violation_photo"
REPORT_FOLDER_NAME = "reports"


async def write_violation_data_on_google_drive(*, chat_id: str,
                                               violation_data: dict,
                                               drive_service: object = None) -> bool:
    """ Загрузка данных на Google Drive

    :param drive_service: объект авторизации
    :param chat_id: id  пользователя / чата
    :param violation_data: данные для записи
    :return:
    """
    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return False

    if not drive_service:
        drive_service = await drive_account_auth_with_oauth2client()

    violation_file_id = await upload_file_on_gdrave(chat_id=chat_id,
                                                    drive_service=drive_service,
                                                    parent=violation_data["json_folder_id"],
                                                    file_path=violation_data['json_full_name'])

    await get_user_permissions(drive_service, file_id=violation_file_id)

    await move_file(drive_service,
                    file_id=violation_file_id,
                    add_parents=violation_data["json_folder_id"],
                    remove_parents=violation_data["report_folder_id"])

    photo_file_id = await upload_file_on_gdrave(chat_id=chat_id,
                                                drive_service=drive_service,
                                                parent=violation_data["photo_folder_id"],
                                                file_path=violation_data['photo_full_name'])

    await get_user_permissions(drive_service, file_id=photo_file_id)

    await move_file(drive_service,
                    file_id=photo_file_id,
                    add_parents=violation_data["photo_folder_id"],
                    remove_parents=violation_data["report_folder_id"])

    return True


async def update_user_violation_data_on_google_drive(*, chat_id: str, violation_data: dict,
                                                     drive_service: object = None,
                                                     file_full_name: str = None,
                                                     notify_user: bool = True):
    """Обновление данных на Google Drive
    поиск файла на google_drive -> удаление файла -> запись откорректированных данных

    :param notify_user: bool оповещение пользователя о загрузке
    :param file_full_name: полный путь к файлу с данными
    :param drive_service: объект авторизации:
    :param chat_id: id пользователя / чата
    :param violation_data: данные для записи
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

    root_folder_id: str = violation_data.get('root_folder_id', None)
    user_folder_id: str = violation_data.get('user_folder_id', None)
    json_folder_id: str = violation_data.get('json_folder_id', None)

    if not violation_data.get('root_folder_id', None) and not violation_data.get('user_folder_id', None):
        root_folder_id: str = await get_root_folder_id(
            drive_service=drive_service,
            root_folder_name=ROOT_REPORT_FOLDER_NAME
        )
    if not root_folder_id:
        return

    if not violation_data.get('user_folder_id', None):
        user_folder_id: str = await get_user_folder_id(
            drive_service=drive_service,
            root_folder_name=str(chat_id),
            parent_id=root_folder_id,
        )
        violation_data['user_folder_id'] = user_folder_id
    if not user_folder_id:
        return

    if not violation_data.get('json_folder_id', None):
        json_folder_id: str = await get_json_folder_id(
            drive_service=drive_service,
            json_folder_name=JSON_FOLDER_NAME,
            parent_id=user_folder_id,
            root_json_folder_id=user_folder_id
        )
        violation_data['violation_data'] = json_folder_id

    await del_by_name_old_data_google_drive(
        chat_id=chat_id,
        drive_service=drive_service,
        name=REPORT_NAME + violation_data["file_id"],
        parent=violation_data["json_folder_id"]
    )

    if not file_full_name:
        file_full_name = violation_data['json_full_name']

    await write_json_violation_user_file(
        data=violation_data,
        json_full_name=file_full_name
    )

    violation_file_id: str = await upload_file_on_gdrave(
        chat_id=chat_id,
        drive_service=drive_service,
        parent=violation_data["json_folder_id"],
        file_path=file_full_name,
        notify_user=notify_user
    )

    await get_user_permissions(
        drive_service=drive_service,
        file_id=violation_file_id
    )

    await move_file(
        service=drive_service,
        file_id=violation_file_id,
        add_parents=json_folder_id,
        remove_parents=root_folder_id
    )

    return True
