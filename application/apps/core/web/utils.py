import asyncio
import os
from pathlib import Path

from apps.core.database.DataBase import DataBase, upload_from_local
from apps.core.database.category_id_transform import CATEGORY_ID_TRANSFORM
from apps.core.bot.handlers.correct_entries.correct_entries_handler import del_file, del_file_from_gdrive
from apps.core.bot.messages.messages import Messages
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import drive_account_credentials
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.set_user_violation_data_on_google_drave import \
    update_user_violation_data_on_google_drive
from apps.core.utils.json_worker.read_json_file import read_json_file
from apps.core.utils.json_worker.writer_json_file import write_json
from apps.core.utils.secondary_functions.get_filepath import get_json_full_filename

from config.config import WRITE_DATA_ON_GOOGLE_DRIVE
from loader import logger

DIRECTORY = Path(__file__).resolve().parent
LOCAL_MEDIA_STORAGE = str(DIRECTORY.parent.parent.parent) + '/media'


class MyMixin(object):
    """Миксина дополнения классов

    """
    mixin_prop = ''

    def get_prop(self):
        return self.mixin_prop.upper()

    def get_upper(self, s):
        """Приведение к верхнему регистру"""
        if isinstance(s, str):
            return s.upper()
        else:
            return s.title.upper()


async def delete_violation_files_from_gdrive(violation: dict):
    """Удаление данных violation из Google Drive

    :param violation dict данные записи для удаления
    """

    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return False

    name: str = violation.get("file_id")
    violation_data_file = LOCAL_MEDIA_STORAGE + str(violation['json'])
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


async def delete_violation_files_from_pc(violation: dict):
    """Удаление данных violation из локального репозитория

    :param violation dict данные записи для удаления
    """
    json_full_path = LOCAL_MEDIA_STORAGE + str(violation['json'])

    if not await del_file(path=json_full_path):
        logger.error(Messages.Error.file_not_found)
    logger.info(Messages.Removed.violation_data_pc)

    photo_full_path = LOCAL_MEDIA_STORAGE + str(violation['photo'])

    if not await del_file(path=photo_full_path):
        logger.error(Messages.Error.file_not_found)
    logger.info(Messages.Removed.violation_photo_pc)


async def del_violations_from_db(violation: dict) -> list:
    """Удаление данных violation из Database

    :param violation dict данные записи для удаления
    """

    file_id = violation['file_id']
    result = DataBase().delete_single_violation(file_id=file_id)
    return result


async def get_id_registered_users() -> list[str]:
    """Получение id зарегистрированных пользователей из json файлов в локальном репозитории

    :return: list[str] список директорий
    """
    return os.listdir(LOCAL_MEDIA_STORAGE)


async def get_params(id_registered_users: list) -> list[dict]:
    """Получение параметров для зарегистрированных пользователей

    :param id_registered_users: список зарегистрированных пользователей,
    :return: параметры для пользователей
    list[{
        'all_files': True,
        'file_path': ...
        'user_file': ...}
    ]
    """
    user_params = []
    for item in id_registered_users:
        if str.isnumeric(item):
            params: dict = {
                'all_files': True,
                'file_path': f"C:/Users/KDeusEx/PycharmProjects/SWTS/application/media/{item}/data_file/",
                'user_file': f"C:/Users/KDeusEx/PycharmProjects/SWTS/application/media/{item}/{item}.json"
            }
            user_params.append(params)

    return user_params


async def update_violation_files_from_gdrive(data_for_update: dict = None):
    """Обновление данных violation в Google Drive

    :param data_for_update dict данные записи для обновления
    """

    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return False

    user_id: str = str(data_for_update.get('user_id'))
    file_id: str = str(data_for_update.get('file_id'))
    date: str = str(file_id).split("___")[0]

    file_full_name = LOCAL_MEDIA_STORAGE + f'/{user_id}/data_file/{date}/json/report_data___{file_id}.json'

    await update_user_violation_data_on_google_drive(
        chat_id=user_id,
        violation_data=data_for_update,
        file_full_name=file_full_name,
        notify_user=False
    )

    logger.info(f'данные обновлены в Google Drive!')


async def check_data_before_update(request_data: dict = None) -> dict:
    """Проверка данных data ( request.POST )

    :param request_data: dict с данными из request.POST
    :return: dict с данными записи
    """
    user_id = request_data.get('user_id', None)
    if not user_id:
        logger.error(f'Not found user_id {user_id}')
        return {}

    file_id = request_data.get('file_id', None)
    if not user_id:
        logger.error(f'Not found file_id {file_id}')
        return {}

    return request_data


async def check_key(violation_data_for_check: dict, key: str) -> bool:
    """Проверка наличие key in violation_data

    :param key: ключ словаря
    :param violation_data_for_check данные для проверки
    :return: True if key in violation_data or False
    """
    if key in [
        'photo', 'json', 'csrfmiddlewaretoken',
        'is_published', 'is_finished', 'title',
    ]:
        return False

    if not violation_data_for_check.get(key, None):
        logger.error(f'Not found {key} in data')

    if key in [k for k, v in CATEGORY_ID_TRANSFORM.items()]:

        db_table_name = CATEGORY_ID_TRANSFORM.get(key, None)

        if db_table_name:
            return True

        logger.error(f'Not found table_name {key} in CATEGORY_ID_TRANSFORM')
        return False

    return False


async def generation_query(key: str, id_item: int) -> str:
    """Формирование запроса в базу данных в определённую таблицу

    :param id_item: id записи,
    :param key: имя категории для поиска соответствующей таблицы в database,
    :return: str сформированный запрос в базу данных,
    """

    if not key:
        logger.error(f"key {key} is None")
        return ''

    try:
        value_int: int = int(id_item)
    except ValueError:
        logger.error(f"id_item {id_item} does not require conversion")
        return ''

    if not isinstance(value_int, int):
        logger.error(f"id_item {id_item} does not require conversion")
        return ''

    db_table_name = CATEGORY_ID_TRANSFORM.get(key, None)
    table_name = db_table_name['table']

    query: str = f'SELECT `title` FROM {table_name} WHERE id = {id_item}'

    return query


async def conversion_value(key: str, value: str) -> str:
    """Преобразование значений вида value:int = 1 в value: str = "..."

    :param value: int or str - значение для нормализации
    :param key: str ключ словаря
    """
    try:
        value_int: int = int(value)
    except ValueError:
        logger.error(f"id_item {value} does not require conversion")
        return value

    if not isinstance(value_int, int):
        logger.error(f"id_item {value} does not require conversion")
        return value

    if key in [k for k, v in CATEGORY_ID_TRANSFORM.items()]:

        db_table_name: dict = CATEGORY_ID_TRANSFORM.get(key, None)
        table_name: str = db_table_name['table']
        if not table_name:
            logger.error(f'Not found table_name {key} in ALL_CATEGORY_IN_DB')
            return value

    query: str = await generation_query(key=key, id_item=value)
    if not query:
        return value

    datas_query: list = DataBase().get_data_list(query=query)
    value = datas_query[0][0]
    logger.debug(f'retrieved data from database: {datas_query}')

    return value


async def get_data_for_update(data: dict, get_from: str = 'local') -> dict:
    """Получение данных из локального репозитория (local) или из базы данных (data_base)

    :param get_from: (local) or (data_base)
    :param data: данные из формы
    :return: dict
    """

    if get_from == 'local':

        user_id: str = str(data.get('user_id'))
        file_id: str = str(data.get('file_id'))
        date: str = str(file_id).split("___")[0]
        json_full_path: str = LOCAL_MEDIA_STORAGE + f'/{user_id}/data_file/{date}/json/report_data___{file_id}.json'

        if not os.path.isfile(json_full_path):
            logger.error(f'Not found file {file_id}')
            return {}
        return await read_json_file(file=json_full_path)

    if get_from == 'data_base':
        try:
            if DataBase().violation_exists(data.get('file_id')):
                violation_list: list = DataBase().get_single_violation(file_id=data.get('file_id'))

                headers: list[str] = [row[1] for row in DataBase().get_table_headers()]
                violation_dict: dict = dict(zip(headers, violation_list[0]))
                return violation_dict

        except Exception as err:
            logger.error(f"Error add_violation in database() : {repr(err)}")
            return {}


async def normalize_violation_data(data_from_form: dict, received_data: dict) -> dict:
    """Нормализация данных

    :param data_from_form: данные из формы
    :param received_data: данные для нормализации
    """
    for key, value in data_from_form.items():
        logger.info(f'{key = }')

        if key + '_id' in [v['column'] for k, v in CATEGORY_ID_TRANSFORM.items()]:
            received_data.pop(key + '_id')
            received_data[key] = value

        if not await check_key(received_data, key):
            received_data[key] = value
            continue

        value = await conversion_value(key=key, value=value)

        received_data[key] = value

    return received_data


async def update_violation_files_from_local(data: dict = None):
    """Обновление данных violation в локальном репозитории

    :param data dict данные записи
    """

    date = data['file_id'].split('___')[0]
    file_name = data['file_id']
    user_id = data['user_id']

    name = await get_json_full_filename(user_id=user_id, file_name=file_name, date=date)

    await write_json(name=name, data=data)

    logger.info(f'данные обновлены в local storage!')


async def update_violations_from_db(data: dict = None):
    """Обновление данных violation в Database

    :param data dict данные записи для обновления
    """

    file_id = data.get('file_id')
    if not DataBase().violation_exists(file_id=file_id):
        logger.error(f"Запись {file_id} не найдена")
        return

    vi_id = DataBase().get_id_violation(file_id=file_id)

    for key, value in data.items():
        if key in ['id', 'photo', 'file', 'json', 'csrfmiddlewaretoken']:
            continue

        if key in [k for k, v in CATEGORY_ID_TRANSFORM.items()]:
            value = DataBase().get_id(
                table=CATEGORY_ID_TRANSFORM[key]['table'],
                entry=value,
                file_id=file_id,
                name=key
            )
            key = key + '_id'

        DataBase().update_column_value(
            column_name=key,
            value=value,
            id=str(vi_id)
        )

    logger.info(f'данные обновлены в database!')


async def get_violation_data_to_update(data_from_form: dict) -> dict:
    """Проверка, обработка и нормализация данных их формы ViolationsForm

    :return: dict нормализованные данные
    """

    verified_data: dict = await check_data_before_update(request_data=data_from_form)
    if not verified_data: return {}

    received_data: dict = await get_data_for_update(data=verified_data, get_from='data_base')
    if not received_data: return {}

    normalize_data: dict = await normalize_violation_data(data_from_form=data_from_form, received_data=received_data)
    if not normalize_data: return {}

    return normalize_data


async def update_violations_from_all_repo(data_from_form: dict = None) -> bool:
    """Обновление данных в базе данных, в локальном репозитории, в Google Drive

    :param data_from_form dict request.POST с данными из формы ViolationsForm с данными для обновления записи и файлов
    :return: bool
    """
    if not isinstance(data_from_form, dict):
        logger.error(f'data: dict не содержит данных!')
        return False

    logger.debug(data_from_form)

    normalize_data = await get_violation_data_to_update(data_from_form)
    if not normalize_data:
        logger.error(f'data: violation_data не содержит данных!')
        return False

    # TODO проверить переключатели is_finished is_published

    await update_violations_from_db(data=normalize_data)

    await update_violation_files_from_local(data=normalize_data)

    await update_violation_files_from_gdrive(data_for_update=normalize_data)

    return True


async def delete_violations_from_all_repo(violation_file_id: str) -> bool:
    """Удаление записи по id из Google Drive, local storage, db

    :param violation_file_id: id записи для удаления
    :return: bool True если успешно or False если не успешно
    """
    if not violation_file_id:
        logger.error(f'violation: {violation_file_id} - запись не найдена')

    violation_list: list = DataBase().get_single_violation(file_id=violation_file_id)
    if not violation_list:
        logger.error(f'violation: {violation_file_id} - запись не найдена')
        return False

    headers = [row[1] for row in DataBase().get_table_headers()]
    violation_dict = dict(zip(headers, violation_list[0]))

    await delete_violation_files_from_gdrive(violation=violation_dict)

    await delete_violation_files_from_pc(violation=violation_dict)

    await del_violations_from_db(violation=violation_dict)

    return True


async def test():
    content = await get_id_registered_users()
    params = await get_params(content)
    logger.info(content)

    for param in params:
        await upload_from_local(params=param)
        logger.info(f'Данные загружены в БД')


if __name__ == "__main__":
    data = {
        'function': 'Специалист 2й категории',
        'location': '18',
        'name': 'Коршаков Алексей Сергеевич',
        'work_shift': '1',
        'main_category': '4',
        'status': '2',
        'is_published': 'on',
        'incident_level': '1',
        'act_required': '2',
        'is_finished': 'on',
        'description': 'кря',
        'comment': 'кря кря',
        'general_contractor': '66',
        'category': '22',
        'violation_category': '3',
        'elimination_time': '4',
        'title': 'кря кря кря',
        'user_id': '373084462',
        'file_id': '13.08.2022___373084462___22954',
        'photo': '',
        'json': '',
        'csrfmiddlewaretoken': 'gHXxcLmKXBSqzLqNRoGhNJFvJRzbpoimqEa05O51xkW8rnJ33R0e9GR81oEDlt9C',

    }

    asyncio.run(update_violations_from_all_repo(data_from_form=data))
