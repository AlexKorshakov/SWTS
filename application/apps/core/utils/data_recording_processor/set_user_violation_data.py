import asyncio
from pprint import pprint

from aiogram import types
from aiogram.types import ReplyKeyboardRemove

import apps.core.bot.data.board_config
from apps.MyBot import MyBot
from apps.core.database.DataBase import DataBase
from apps.core.database.entry_in_db import write_data_in_database
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import violation_data
from apps.core.utils.bot_utils_processor.del_messege import cyclical_deletion_message
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.set_user_violation_data_on_google_drave import \
    write_violation_data_on_google_drive
from apps.core.utils.json_worker.writer_json_file import write_json_violation_user_file
from loader import logger


async def pre_set_violation_data(message: types.Message):
    """Интерфейс записи нарушения на Google Drive

    """
    chat_id = message.from_user.id
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Report.begin)

    stop_violation_id = apps.core.bot.data.board_config.stop_violation_mes_id = message.message_id + 3
    logger.info(f"start_violation message.from_user.id {stop_violation_id}")

    pprint(f'{violation_data = }')

    # drive_service = await drive_account_auth_with_oauth2client()
    # data: dict = await get_folders_ids_from_google_drive(user=chat_id, drive_service=drive_service)
    #
    # if not await preparing_violation_data_for_loading_to_google_drive(data=data):
    #     return False

    pprint(f'{violation_data = }')

    await set_violation_data(chat_id=chat_id)

    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.Report.completed_successfully)
    await MyBot.dp.bot.send_message(chat_id=chat_id, text=Messages.help_message, reply_markup=ReplyKeyboardRemove())

    await cyclical_deletion_message(chat_id=chat_id)


async def set_violation_data(*, chat_id: str):
    """Запись и сохранение данных в local storage, database, Google Drive
    """

    pprint(f'{violation_data = }')
    pprint(f'{violation_data.get("json_full_name", None) = }')

    if await write_json_violation_user_file(data=violation_data):
        logger.info(f"Данные сохранены в local storage {violation_data['json_full_name']}")

    if await write_violation_data_on_google_drive(chat_id=chat_id, violation_data=violation_data):
        logger.info(f"Данные сохранены в Google Drive в директорию \n"
                    f"https://drive.google.com/drive/folders/{violation_data['json_folder_id']}")

    if await write_data_in_database(violation_data=violation_data):
        logger.info(f"Данные сохранены в database в файл {DataBase().db_file}")


async def test():
    violation_data = {
        "act_required": "Требуется*",
        "category": "Отходы",
        "comment": "Убрать мусор строительный",
        "data": "30:11:2022",
        "day": "30",
        "day_of_year": "334",
        "description": "Захламление строительным мусором",
        "elimination_time": "3 дня",
        "file_id": "30.11.2022___862629360___29431",
        "function": "специалист",
        "general_contractor": "ООО Ренейссанс Хэви Индастрис",
        "hse_id": 2,
        "incident_level": "Без последствий",
        "json_file_path": "C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\862629360\\data_file\\30.11.2022\\json\\",
        "json_full_name": "C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\862629360\\data_file\\30.11.2022\\json\\report_data___30.11.2022___862629360___29431.json",
        "location": "ПО - 1",
        "main_category": "Экология",
        "main_location": "ТК",
        "month": "11",
        "name": "Гарифуллин Ильгиз Рамилевич",
        "normative_documents": "Захламление территории производства работ строительным отходами",
        "normative_documents_normative": "Приказ №883н от 11 декабря 2020 года «Об утверждении Правил по охране труда при строительстве, реконструкции и ремонте» п. 41",
        "normative_documents_procedure": "Привести в соответствие с требованиями НД",
        "now": "2022-11-30 11:17:01.702504",
        "parent_id": None,
        "photo_file_path": "C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\862629360\\data_file\\30.11.2022\\photo\\",
        "photo_full_name": "C:\\Users\\KDeusEx\\PycharmProjects\\SWTS\\application\\media\\862629360\\data_file\\30.11.2022\\photo\\report_data___30.11.2022___862629360___29431.jpg",
        "quarter": "04",
        "status": "В работе",
        "sub_location": "4.0.6. Корпус обогащения",
        "user_fullname": "Ильгиз Гарифуллин",
        "user_id": 862629360,
        "violation_category": "Опасная ситуация*",
        "violation_id": 29431,
        "week": "48",
        "work_shift": "Дневная смена",
        "year": "2022"
    }

    location = DataBase().get_dict_data_from_table_from_id(
        table_name='core_location',
        id=2
    )
    location = location['title']
    print(f'{location = }')

    await write_data_in_database(violation_data=violation_data)


if __name__ == "__main__":
    asyncio.run(test())
