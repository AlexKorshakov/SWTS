import asyncio
from pprint import pprint

from aiogram import types

from aiogram.dispatcher import FSMContext
# from apps.core.bot.reports.report_data import violation_data
from apps.core.bot.reports.report_data_preparation import set_violation_atr_data
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import (
    drive_account_auth_with_oauth2client,
    drive_account_credentials,
    move_file)
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.find_folder import find_folder_with_name_on_google_drive
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.folders_creator import create_directory_on_google_drive
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.set_permissions import gaining_access_drive
from config.config import ROOT_REPORT_FOLDER_NAME
from loader import logger

from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import (
    drive_account_auth_with_oauth2client,
    drive_account_credentials)
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.get_folder_id import (get_root_folder_id,
                                                                                  get_user_folder_id)

WORK_ON_HEROKU: bool = False
WORK_ON_PC: bool = True

ROOT_REPORT_FOLDER_NAME: str = "MosIng_HSE_repots"
ROOT_REPORT_FOLDER_ID: str = '1n4M_LHDG_QQ4EFuDYxQLe_MaK-k3wv96'


async def write_data_on_google_drive(message: types.Message, state: FSMContext):
    """Сохранение данных в облако Google Drive
    """

    chat_id = message.chat.id
    drive_service = None

    if WORK_ON_HEROKU:
        drive_service = await drive_account_auth_with_oauth2client()

    if WORK_ON_PC:
        drive_service = await drive_account_credentials()

    if not drive_service:
        logger.info(f"**drive_service {drive_service} in Google Drive.**")
        return

    root_folder_id = await get_root_folder_id(drive_service, ROOT_REPORT_FOLDER_NAME)

    folder_id = await get_user_folder_id(drive_service,
                                         root_folder_name=str(chat_id),
                                         parent_id=root_folder_id)

    # violation_data["folder_id"] = folder_id
    await set_violation_atr_data("folder_id", folder_id, state=state)

    top = drive_service.files().get(fileId=folder_id).execute()
    await asyncio.sleep(2)
    stack = [((top['name'],), [top])]
    pprint(stack)


async def get_report_folder_id(drive_service, report_folder_name: str, parent_id=None, root_report_folder_id=None):
    """Создание основной директории хранения report в директории пользователя на Google Drive
    """
    report_folder_id = await find_folder_with_name_on_google_drive(
        drive_service=drive_service,
        name=str(report_folder_name),
        parent=parent_id
    )

    if not report_folder_id:
        report_folder_id = await create_directory_on_google_drive(
            drive_service=drive_service,
            directory_name=str(report_folder_name),
            parent_id=parent_id
        )
        await asyncio.sleep(2)
        await gaining_access_drive(service=drive_service, folder_id=report_folder_id)
        await move_file(
            service=drive_service,
            file_id=report_folder_id,
            add_parents=parent_id,
            remove_parents=root_report_folder_id
        )
        return report_folder_id

    logger.debug(f"**Find  https://drive.google.com/drive/folders/{report_folder_id} in Google Drive.**")

    return report_folder_id


async def get_photo_folder_id(drive_service, photo_folder_name: str, parent_id=None, root_photo_folder_id=None):
    """Создание основной директории хранения photo в директории пользователя на Google Drive
    """
    photo_folder_id = await find_folder_with_name_on_google_drive(
        drive_service=drive_service,
        name=str(photo_folder_name),
        parent=parent_id
    )

    if not photo_folder_id:
        photo_folder_id = await create_directory_on_google_drive(
            drive_service=drive_service,
            directory_name=str(photo_folder_name),
            parent_id=parent_id
        )
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=photo_folder_id)
        await move_file(
            service=drive_service,
            file_id=photo_folder_id,
            add_parents=parent_id,
            remove_parents=root_photo_folder_id
        )
        return photo_folder_id

    logger.debug(f"**Find https://drive.google.com/drive/folders/{photo_folder_id} in Google Drive.**")

    return photo_folder_id


async def get_json_folder_id(drive_service: object, json_folder_name: str, parent_id: str = None,
                             root_json_folder_id: str = None) -> str:
    """Поиск и получение json_folder_id из parent_id
    если не найдено - создается директория хранения json в директории root_json_folder_id на Google Drive

    :param root_json_folder_id: options
    :param parent_id: options
    :param json_folder_name:
    :param drive_service
    :return: json_folder_id:str
    """
    json_folder_id: str = await find_folder_with_name_on_google_drive(
        drive_service=drive_service,
        name=str(json_folder_name),
        parent=parent_id
    )

    if not json_folder_id:
        json_folder_id = await create_directory_on_google_drive(
            drive_service=drive_service,
            directory_name=str(json_folder_name),
            parent_id=parent_id
        )
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=json_folder_id)
        await move_file(service=drive_service,
                        file_id=json_folder_id,
                        add_parents=parent_id,
                        remove_parents=root_json_folder_id
                        )
        return json_folder_id

    logger.debug(f"**Find  https://drive.google.com/drive/folders/{json_folder_id} in Google Drive.**")

    return json_folder_id


async def get_root_folder_id(drive_service: object, root_folder_name: str):
    """Создание основной директории в корневой директории Google Drive

    :param root_folder_name: имя директории
    :param drive_service: объект авторизации
    """
    root_folder_id = await find_folder_with_name_on_google_drive(
        drive_service=drive_service,
        name=str(root_folder_name)
    )

    if not root_folder_id:
        root_folder_id = await create_directory_on_google_drive(
            drive_service=drive_service,
            directory_name=str(root_folder_name)
        )
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=root_folder_id)
        return root_folder_id

    logger.debug(f"**Find  https://drive.google.com/drive/folders/{root_folder_id} in Google Drive.**")

    return root_folder_id


async def get_user_folder_id(drive_service, root_folder_name: str, parent_id):
    """Создание директории в родительской директории
    """
    user_folder_id = await find_folder_with_name_on_google_drive(
        drive_service=drive_service,
        name=str(root_folder_name),
        parent=parent_id
    )

    if not user_folder_id:
        user_folder_id = await create_directory_on_google_drive(
            drive_service=drive_service,
            directory_name=str(root_folder_name),
            parent_id=parent_id
        )
        await asyncio.sleep(2)
        await gaining_access_drive(drive_service, folder_id=user_folder_id)
        return user_folder_id

    logger.debug(f"**Find  https://drive.google.com/drive/folders/{user_folder_id} in Google Drive.**")

    return user_folder_id


if __name__ == "__main__":
    asyncio.run(write_data_on_google_drive("message"))
