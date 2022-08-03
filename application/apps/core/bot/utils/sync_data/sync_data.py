import asyncio
import os
from pathlib import Path
from pprint import pprint

from apps.core.bot.database.DataBase import create_file_path
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.GoogleDriveWorker import drive_account_auth_with_oauth2client, \
    move_file
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.download_file_for_google_drive import download_file
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.find_folder import find_file_by_name, \
    find_files_or_folders_list_by_parent_id
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.get_folder_id import get_root_folder_id
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.set_permissions import get_user_permissions
from apps.core.bot.utils.goolgedrive.GoogleDriveUtils.upload_data_on_gdrive import upload_file_on_gdrave
from apps.core.bot.utils.goolgedrive.googledrive_worker import ROOT_REPORT_FOLDER_NAME
from apps.core.bot.utils.secondary_functions.get_json_files import get_dirs_files, get_files
from apps.core.bot.utils.set_user_violation_data import preparing_data_for_loading

BASE_DIR = Path(__file__).resolve()


async def get_id_item(item):
    debug = False
    if 'report_data' in item:
        id_item = item.split('___')[-2]
    else:
        id_item = item.split('.')[-2]

    if debug: print(f'{item} {id_item = }')
    return id_item


async def get_normalize_file_list(file_list):
    return [f.split('\\')[-1] for f in file_list]


async def get_violations_file_list(directory: str) -> list:
    """Получение списка файлов с нарушениям / регистрационными данными"""
    debug = False

    if debug: print(f'{directory = }')

    if not os.path.isdir(directory):
        return []

    dirs = await get_dirs_files(directory=directory)

    file_list = []
    for f_dir in dirs:
        file_path = f'{directory}\\{f_dir}'

        if os.path.isdir(file_path):
            json_file_list = await get_files(file_path, endswith=".json")
            file_list = file_list + json_file_list

    if debug:
        for n, i in enumerate(file_list): print(f'{n} {i}')

    return file_list


async def download_file_on_google_disc(drive_service, preparing_data, file_path, parent, id_item):
    violation_file_id = await upload_file_on_gdrave(
        chat_id=id_item,
        drive_service=drive_service,
        parent=parent,
        file_path=file_path
    )

    await get_user_permissions(drive_service=drive_service, file_id=violation_file_id)

    await move_file(
        service=drive_service,
        file_id=violation_file_id,
        add_parents=preparing_data["json_folder_id"],
        remove_parents=preparing_data["report_folder_id"]
    )


async def get_file_location_map(drive_service) -> list:
    root_folder_id = await get_root_folder_id(
        drive_service=drive_service,
        root_folder_name=ROOT_REPORT_FOLDER_NAME
    )

    folders_list = await find_files_or_folders_list_by_parent_id(
        drive_service, folder_id=root_folder_id, is_folder=True
    )

    data_list = []
    for item in folders_list:
        folder_id = item['id']
        folder_list = await find_files_or_folders_list_by_parent_id(
            drive_service, folder_id=folder_id, is_folder=True, mime_type='application/vnd.google-apps.folder'
        )
        file_list = await find_files_or_folders_list_by_parent_id(
            drive_service, folder_id=folder_id, is_folder=False, mime_type='application/json'
        )

        data_list.append(
            {
                'user': item,
                'reg_file': file_list[0],
                'folder_list': folder_list
            }
        )

    return data_list


async def get_global_file_list(drive_service, file_location_map):
    global_file_list = []
    for item in file_location_map:
        user_file_list = []
        for type_files in item['folder_list']:
            file_list = []
            if type_files['name'] == 'reports':
                file_list = await find_files_or_folders_list_by_parent_id(
                    drive_service, folder_id=type_files['id'],
                    is_folder=False, mime_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
            if type_files['name'] == 'violation_photo':
                file_list = await find_files_or_folders_list_by_parent_id(
                    drive_service, folder_id=type_files['id'],
                    is_folder=False, mime_type='image/jpeg'
                )
            if type_files['name'] == 'violation_json':
                file_list = await find_files_or_folders_list_by_parent_id(
                    drive_service, folder_id=type_files['id'],
                    is_folder=False, mime_type='application/json'
                )
            user_file_list.append(file_list)

        global_file_list.append(user_file_list)

    return global_file_list


async def normalize_global_file_list(file_list):
    reports, photos, json_files = [], [], []

    for item in file_list:
        if not item: continue

        reports.extend(item[0])
        photos.extend(item[1])
        json_files.extend(item[2])

    return reports, photos, json_files


async def get_local_files_for_sync():
    directory = os.path.join(BASE_DIR.parent.parent.parent.parent.parent.parent, 'media')
    file_list = await get_violations_file_list(directory=directory)
    normalize_file_list = await get_normalize_file_list(file_list)

    return file_list, normalize_file_list


async def local_to_google_drive(file_list, normalize_file_list):
    """Синхронизация media -> google_drive"""

    debug = False

    # directory = os.path.join(BASE_DIR.parent.parent.parent.parent.parent.parent, 'media')
    # file_list = await get_violations_file_list(directory=directory)
    # normalize_file_list = await get_normalize_file_list(file_list)

    if not normalize_file_list: return

    last_id = None
    preparing_data = {}

    drive_service = await drive_account_auth_with_oauth2client()
    if not drive_service:
        if debug: print(f"🔒 **drive_service {drive_service} in Google Drive.**")
        return

    for item in normalize_file_list:

        id_item = await get_id_item(item)
        if not id_item: continue

        if last_id != id_item:
            last_id = id_item
            preparing_data: dict = await preparing_data_for_loading(drive_service=drive_service, chat_id=id_item)
            parent = preparing_data['user_folder_id']
        else:
            parent = preparing_data['json_folder_id']

        result: list = await find_file_by_name(service=drive_service, name=item, parent=parent)
        if debug: pprint(result)

        if not result:
            file_path = [i for i in file_list if item in i][0]

            await download_file_on_google_disc(drive_service=drive_service, preparing_data=preparing_data,
                                               file_path=file_path, parent=parent, id_item=id_item)


async def google_drive_to_local(file_list, local_files):
    """Синхронизация google_drive -> media"""

    drive_service = await drive_account_auth_with_oauth2client()

    file_location_map = await get_file_location_map(drive_service=drive_service)

    # pprint(file_location_map)

    global_file_list = await get_global_file_list(
        drive_service=drive_service, file_location_map=file_location_map
    )

    reports, photos, json_files = await normalize_global_file_list(global_file_list)

    # pprint(json_files)

    synced, download = 0, 0

    for n, i in enumerate(json_files, start=1):

        if i['name'] in local_files:
            synced = synced + 1
            print(f'{n} file: {i} is synced')
        else:
            download = download + 1
            print(f'{n} file: {i} need download')

            directory = os.path.join(BASE_DIR.parent.parent.parent.parent.parent.parent, 'media')
            file_path = f'{directory}\\{i["name"].split("___")[2]}\\data_file\\{i["name"].split("___")[1]}\\json\\'

            await create_file_path(path=file_path)
            await download_file(service=drive_service, file_id=i["id"], file_name=file_path + i["name"])

    print(f'Total: {len(json_files)} synced: {synced} need download {download}')


async def run_sync():
    file_list, local_files = await get_local_files_for_sync()
    # await local_to_google_drive(file_list, local_files)
    await google_drive_to_local(file_list, local_files)


if __name__ == '__main__':
    # asyncio.run(local_to_google_drive())
    asyncio.run(run_sync())
