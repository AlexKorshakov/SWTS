import asyncio
import os
from pathlib import Path

from apps.core.bot.database.DataBase import DataBase, run
from apps.core.bot.handlers.correct_entries.correct_entries_handler import del_file, del_file_from_gdrive
from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_credentials
from loader import logger

DIRECTORY = Path(__file__).resolve().parent


class MyMixin(object):
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()

    def get_upper(self, s):
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()


async def del_violations(violation_file_id: str) -> bool:
    if violation_file_id:
        violation_list: list = DataBase().get_violation(violation_file_id)
        if not violation_list:
            logger.info(f'{violation_file_id = } запись не найдена')
            return True

        rows = [row[1] for row in DataBase().get_table_info()]
        violation_dict = dict(zip(rows, violation_list[0]))

        await delete_violation_files_from_gdrive(violation=violation_dict)

        await delete_violation_files_from_pc(violation=violation_dict)

        await del_violations_from_db(violation=violation_dict)

    return True


async def delete_violation_files_from_gdrive(violation: dict):
    name: str = violation.get("file_id")
    violation_data_file = str(DIRECTORY.parent.parent.parent) + '/media' + str(violation['json'])
    violation_json_parent_id = violation['json_folder_id']

    drive_service = await drive_account_credentials()

    if not await del_file_from_gdrive(drive_service=drive_service,
                                      name='report_data___' + name + '.json',
                                      violation_file=violation_data_file,
                                      parent_id=violation_json_parent_id):
        logger.error(Messages.Error.file_not_found)
    logger.info(Messages.Removed.violation_data_gdrive_delete)

    violation_photo_file = violation['photo']
    violation_photo_parent_id = violation['photo_folder_id']

    if not await del_file_from_gdrive(drive_service=drive_service,
                                      name='report_data___' + name + '.jpg',
                                      violation_file=violation_photo_file,
                                      parent_id=violation_photo_parent_id):
        logger.error(Messages.Error.file_not_found)
    logger.info(Messages.Removed.violation_photo_gdrive)


async def delete_violation_files_from_pc(violation):
    json_full_path = str(DIRECTORY.parent.parent.parent) + '/media' + str(violation['json'])

    if not await del_file(path=json_full_path):
        logger.error(Messages.Error.file_not_found)
    logger.info(Messages.Removed.violation_data_pc)

    photo_full_path = str(DIRECTORY.parent.parent.parent) + '/media' + str(violation['photo'])

    if not await del_file(path=photo_full_path):
        logger.error(Messages.Error.file_not_found)
    logger.info(Messages.Removed.violation_photo_pc)


async def del_violations_from_db(violation):
    file_id = violation['file_id']
    result = DataBase().delete_violation(file_id=file_id)
    return result


async def get_id_registered_users():
    return os.listdir(str(DIRECTORY.parent.parent.parent) + '/media')


async def get_params(content):
    user_params = []
    for item in content:
        if str.isnumeric(item):
            params: dict = {
                'all_files': True,
                'file_path': f"C:/Users/KDeusEx/PycharmProjects/SWTS/application/media/{item}/data_file/",
                'user_file': f"C:/Users/KDeusEx/PycharmProjects/SWTS/application/media/{item}/{item}.json"
            }
            user_params.append(params)

    return user_params


async def test():
    content = await get_id_registered_users()
    params = await get_params(content)
    logger.info(content)

    for param in params:
        await run(params=param)
        logger.info(f'Данные загружены в БД')


if __name__ == "__main__":
    # violation_file_id: str = '07.07.2022___373084462___21505'
    #
    # asyncio.run(del_violations(violation_file_id=violation_file_id))
    asyncio.run(test())
