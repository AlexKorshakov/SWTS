import asyncio
import os
import datetime
from os import makedirs
from pprint import pprint

from aiogram import types

from config.web.settings import BASE_DIR
from loader import logger

from config.config import REPORT_NAME
from apps.core.bot.data.report_data import violation_data
from apps.core.utils.json_worker.writer_json_file import write_json_violation_user_file

BOT_MEDIA_PATH = os.path.join(BASE_DIR.parent.parent, 'media\\')


async def date_now() -> str:
    """Возвращает текущую дату в формате дд.мм.гггг
    :return:
    """
    return str((datetime.datetime.now()).strftime("%d.%m.%Y"))


async def get_report_full_filepath(user_id: str = None, actual_date: str = None):
    """Обработчик сообщений с reports
    Получение полного пути файла

    :param actual_date:
    :param user_id:
    """
    if not actual_date:
        actual_date = await date_now()

    return f"{BOT_MEDIA_PATH}{user_id}\\data_file\\{actual_date}\\reports\\"


async def get_registration_full_filepath(user_id: str = None):
    """Обработчик сообщений с registration
    Получение полного пути файла
    """
    return f"{BOT_MEDIA_PATH}{user_id}\\"


async def get_photo_full_filepath(user_id: str = None, actual_date: str = None):
    """Обработчик сообщений с photo
    Получение полного пути файла
    """

    if not actual_date:
        actual_date = await date_now()
    return f"{BOT_MEDIA_PATH}{user_id}\\data_file\\{actual_date}\\photo\\"


async def get_photo_full_filename(user_id: str = None, name=None, date=None):
    """Обработчик сообщений с photo
    Получение полного пути файла
    """
    if not date:
        date = await date_now()
    return f"{BOT_MEDIA_PATH}{user_id}\\data_file\\{date}\\photo\\{REPORT_NAME}{name}.jpg"


async def get_json_full_filepath(user_id: str = None, actual_date: str = None):
    """Обработчик сообщений с json
    Получение полного пути файла
    """
    if not actual_date:
        actual_date = await date_now()

    return f"{BOT_MEDIA_PATH}{user_id}\\data_file\\{actual_date}\\json\\"


async def get_json_full_filename(user_id: str = None, file_name: str = None, date=None):
    """Обработчик сообщений с json
    Получение полного пути файла
    """
    if not date:
        date = await date_now()

    return f"{BOT_MEDIA_PATH}{user_id}\\data_file\\{date}\\json\\{REPORT_NAME}{file_name}.json"


async def create_file_path(path: str):
    """Проверка и создание директории если не существует

    :param path: полный путь к директории,
    :return:
    """
    if not os.path.isdir(path):
        logger.debug(f"user_path: {path} is directory")
        try:
            makedirs(path)
        except Exception as err:
            logger.error(f"makedirs err {repr(err)}")


async def preparation_violations_paths_on_pc(message: types.Message):
    """Создание путей сохранения файлов и запись в json
    :param message:
    :return:
    """
    violation_data["photo_file_path"] = await get_photo_full_filepath(user_id=violation_data["user_id"])
    violation_data["photo_full_name"] = await get_photo_full_filename(user_id=violation_data["user_id"],
                                                                      name=violation_data["file_id"])
    await create_file_path(violation_data["photo_file_path"])
    await message.photo[-1].download(destination=violation_data["photo_full_name"], make_dirs=False)

    violation_data["json_file_path"] = await get_json_full_filepath(user_id=violation_data["user_id"])
    violation_data["json_full_name"] = await get_json_full_filename(user_id=violation_data["user_id"],
                                                                    file_name=violation_data["file_id"])
    await create_file_path(violation_data["json_file_path"])

    await write_json_violation_user_file(data=violation_data)


async def preparation_registration_paths_on_pc(user_id: str, user_data: dict):
    user_data["reg_json_full_name"] = f"{BOT_MEDIA_PATH}{user_id}\\{user_id}.json"
    user_data["json_full_name"] = f"{BOT_MEDIA_PATH}{user_id}\\{user_id}.json"
    user_data["reg_user_path"] = f"{BOT_MEDIA_PATH}{user_id}\\"

    return user_data


async def get_file_path_user_data(chat_id: str):
    return f"{BOT_MEDIA_PATH}{chat_id}\\data_file"


async def get_user_registration_data_json_file(chat_id: str):
    return f"{BOT_MEDIA_PATH}{chat_id}\\{chat_id}.json"


async def get_user_registration_file(user_id: str) -> str:
    return BOT_MEDIA_PATH + user_id


async def get_bot_data_path():
    return f"{BOT_MEDIA_PATH}"


async def get_file_path(file_id: str) -> str:
    """Формирование пути к файлу с регистрационными данными

    Example:

    .. code-block:: python3

        f'{BOT_DATA_PATH}\\{file_id}\\{file_id}.json'
    """
    return f'{BOT_MEDIA_PATH}\\{file_id}\\{file_id}.json'


async def test():
    logger.info(f'date_now: {await date_now()}')
    print(get_report_full_filepath())


async def test2():
    violation_data = {
        'user_id': '373084462',
        'file_id': "01.10.2021___373084462___9493"
    }

    violation_data["photo_file_path"] = await get_photo_full_filepath(user_id=violation_data["user_id"])
    violation_data["photo_full_name"] = await get_photo_full_filename(user_id=violation_data["user_id"],
                                                                      name=violation_data["file_id"])
    await create_file_path(violation_data["photo_file_path"])

    violation_data["json_file_path"] = await get_json_full_filepath(user_id=violation_data["user_id"])
    violation_data["json_full_name"] = await get_json_full_filename(user_id=violation_data["user_id"],
                                                                    file_name=violation_data["file_id"])
    await create_file_path(violation_data["json_file_path"])

    pprint(violation_data)


if __name__ == "__main__":
    asyncio.run(test2())
