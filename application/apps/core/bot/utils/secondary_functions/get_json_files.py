import os

from apps.core.bot.utils.json_worker.read_json_file import read_json_file
from apps.core.bot.utils.secondary_functions.get_filepath import get_bot_data_path, get_file_path


async def get_files(main_path, endswith=".json") -> list:
    """Получение списка json файлов из файловой системы
    """
    json_files = []
    for subdir, dirs, files in os.walk(main_path):
        for file in files:
            filepath = subdir + os.sep + file
            if filepath.endswith(endswith):
                json_files.append(filepath)
    return json_files


async def get_dirs_files(directory) -> list:
    """Получение списка json файлов из файловой системы
    """

    for subdir, dirs, files in os.walk(directory):
        return dirs


async def get_registered_users():
    files: list = await get_dirs_files(await get_bot_data_path())

    users_data: list = []
    for file in files:

        file_path = await get_file_path(file=file)
        if not os.path.isfile(file_path):
            continue

        file_dict: dict = await read_json_file(file_path)

        try:
            name = file_dict['name'].lstrip(' ').rstrip(' ')
        except KeyError:
            name = 'Нет описания'

        user_id: str = f"{file_dict['user_id']} {name.split(' ')[0]}"

        users_data.append(user_id)

    return users_data, files
