from loader import logger

from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.find_folder import find_file_by_name
from apps.core.bot.utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_ID


async def delete_folders(drive_service: object, folder_names: list):
    """Удаление списка папок с GoogleDrive

    :param folder_names: list с объектами для удаления
    :param drive_service: объект авторизации
    :return: logger.info(message)
    """

    if not drive_service:
        logger.error(f'Not find Drive API service instance')
        return

    for item, f_name in enumerate(folder_names):

        if f_name["id"] == ROOT_REPORT_FOLDER_ID:
            continue

        if await delete_folder(
                service=drive_service,
                folder_id=f_name["id"]
        ):
            logger.info(f'Item {item}: delete file/folder {f_name["name"]} id {f_name["id"]}')
        else:
            logger.info(f'Item {item}: not delete file/folder {f_name["name"]} id {f_name["id"]}')


async def delete_folder(service: object, folder_id: str) -> bool:
    """Permanently delete a file, skipping the trash.

    :param service: Drive API service instance.
    :param folder_id: str ID of the file to delete.
    """
    if not service:
        logger.error(f'Not find Drive API service instance')
        return False

    if not folder_id:
        logger.error(f'Not folder_id to delete')
        return False

    try:
        service.files().delete(fileId=folder_id).execute()
        return True

    except Exception as err:
        logger.error(f'An error occurred:{err}')
        return False


async def delete_folders_for_id(drive_service: object, folder_id_list: list):
    """Удаление файлов или папки по id

    :param drive_service: объект авторизации
    :param folder_id_list:
    :return:
    """
    for item, f_id in enumerate(folder_id_list, start=1):

        if f_id["id"] == ROOT_REPORT_FOLDER_ID:
            continue

        if await delete_folder(service=drive_service, folder_id=f_id["id"]):
            logger.info(f'Item {item}: delete file/folder {f_id["name"]} id {f_id["id"]}')


async def del_by_name_old_data_google_drive(*, chat_id: str, drive_service: object, name: str = None,
                                            parent: str = None) -> bool:
    """Удаление старых данных по имени name  из папки parent

    :param parent: родительская директория на goolgedrive
    :param name: options имя файла для удаления
    :param chat_id: id пользователя
    :param drive_service: объект авторизации
    :return: True or False
    """

    if not name:
        name: str = str(chat_id)

    found_files: list = await find_file_by_name(drive_service, name=name, parent=parent)

    if not found_files:
        logger.error(f"File {name = } not found in {parent = } on goolgedrive")
        return False

    await delete_folders_for_id(drive_service, folder_id_list=found_files)
    logger.debug(f"File {name = } delete in {parent = } on goolgedrive")
    return True
