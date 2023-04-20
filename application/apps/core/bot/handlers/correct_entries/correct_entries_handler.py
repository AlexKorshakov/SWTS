import typing

from loader import logger

logger.debug(f"{__name__} start import")
import os
from mimetypes import guess_type
from pprint import pprint

from aiogram import types
from aiogram.dispatcher.filters import Command

from apps.MyBot import MyBot, bot_send_message
from config.config import WRITE_DATA_ON_GOOGLE_DRIVE

from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb
from apps.core.bot.messages.messages import Messages

# from apps.core.utils.generate_report.get_file_list import get_json_file_list
# from apps.core.bot.callbacks.sequential_action.correct_registration_data_answer import get_correct_data
# from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import posts_cb, \
#     add_subtract_inline_keyboard_with_action
# from apps.core.bot.data import board_config
from apps.core.bot.data.category import CORRECT_COMMANDS_LIST
# from apps.core.bot.messages.messages import Messages
# from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import build_inlinekeyboard
# from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.GoogleDriveWorker import drive_account_credentials
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.find_folder import q_request_constructor, \
    params_constructor, \
    find_files_by_params
from apps.core.utils.goolgedrive_processor.GoogleDriveUtils.folders_deleter import delete_folder
from apps.core.utils.misc import rate_limit

logger.debug(f"{__name__} finish import")


# len_description = 25


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('correct_entries'))
async def correct_entries_handler(message: types.Message = None, *, hse_user_id=None):
    """Корректирование уже введённых значений на локальном pc и на google drive

    :return:
    """

    chat_id = message.chat.id if message else hse_user_id
    if not await check_user_access(chat_id=chat_id):
        logger.error(f'access fail {chat_id = }')
        return

    reply_markup = await add_correct_inline_keyboard_with_action()
    text: str = 'Выберите действие'

    await bot_send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


async def add_correct_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton('Незакрытые акты',
                                          callback_data=posts_cb.new(id='-', action='correct_acts')))
    markup.add(types.InlineKeyboardButton('Незакрытые записи не в актах',
                                          callback_data=posts_cb.new(id='-', action='correct_non_act_item')))
    return markup


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['correct_db_items']))
async def call_correct_db_items(call: types.CallbackQuery, callback_data: typing.Dict[str, str]):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    hse_user_id = call.message.chat.id
    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    await MyBot.bot.send_message(chat_id=hse_user_id, text=Messages.Error.error_action)
    logger.error(f'{hse_user_id = } Messages.Error.error_action')

    # await act_generate_handler(call.message)


#     violation_description: list = []
#     violation_files: list = []
#
#     if not await check_user_access(chat_id=chat_id):
#         return
#
#     file_list = await get_json_file_list(chat_id=chat_id)
#
#     if not file_list:
#         logger.warning(Messages.Error.file_list_not_found)
#         await MyBot.bot.send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
#
#     for file_path in file_list:
#         file = await read_json_file(file_path)
#
#         if file is None:
#             continue
#
#         if file.get("violation_id"):
#             violation_id = file.get("violation_id")
#         else:
#             violation_id = file.get("file_id").split(SEPARATOR)[-1]
#         try:
#             if len(file.get('description')) < len_description:
#                 description = file.get('description')[:len(file.get('description'))]
#             else:
#                 description = file.get('description')[:len_description]
#         except TypeError:
#             description = 'нет описания'
#
#         violation_description.append(f"{violation_id} {description}...")
#         violation_files.append(
#             {"violation_id": f"{violation_id}",
#              "description": f"{violation_id} {description}...",
#              "json_full_name": f"{file.get('json_full_name')}",
#              "photo_full_name": f"{file.get('photo_full_name')}"
#              }
#         )
#
#     menu_level = board_config.menu_level = 2
#     board_config.violation_file = violation_files
#     menu_list = board_config.violation_menu_list = violation_description
#
#     registration_button = types.InlineKeyboardButton(
#         text='Данные регистрации',
#         callback_data=posts_cb.new(id='-', action='correct_registration_data')
#     )
#
#     commission_button = types.InlineKeyboardButton(
#         text='Шапка отчета',
#         callback_data=posts_cb.new(id='-', action='correct_commission_composition')
#     )
#
#     reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level,
#                                               addition=[registration_button, commission_button])
#
#     await message.answer(text=Messages.Choose.entry, reply_markup=reply_markup)
#
#
# @MyBot.dp.callback_query_handler(lambda call: call.data in board_config.violation_menu_list)
# async def violation_id_answer(call: types.CallbackQuery):
#     """Обработка ответов содержащихся в board_config.violation_menu_list
#
#     """
#     for item in board_config.violation_menu_list:
#         try:
#             if call.data != item:
#                 continue
#             logger.debug(f"Выбрано: {item}")
#
#             for file in board_config.violation_file:
#                 if file['description'] != item:
#                     continue
#
#                 violation_file = await read_json_file(file['json_full_name'])
#
#                 if not violation_file:
#                     await call.message.answer(text=Messages.Error.file_not_found)
#                     continue
#
#                 try:
#                     logger.info(f"**Find  https://drive.google.com/drive/folders/{violation_file['json_folder_id']} "
#                                 f"in Google Drive.**")
#                     logger.info(f"**Find  https://drive.google.com/drive/folders/{violation_file['photo_folder_id']} "
#                                 f"in Google Drive.**")
#                 except KeyError as key_err:
#                     logger.error(f"key_err: {repr(key_err)}")
#
#                 board_config.current_file = item
#
#                 reply_markup = await add_subtract_inline_keyboard_with_action()
#                 await call.message.answer(text=Messages.Admin.answer, reply_markup=reply_markup)
#
#                 break
#
#             break
#
#         except Exception as callback_err:
#             logger.error(f"{repr(callback_err)}")
#
#
# @MyBot.dp.callback_query_handler(lambda call: call.data in CORRECT_COMMANDS_LIST)
# async def act_required(call: types.CallbackQuery):
#     """Обработка ответов содержащихся в CORRECT_COMMANDS_LIST
#     """
#
#     chat_id = call.message.chat.id
#     correct_data = await get_correct_data(chat_id=chat_id, call=call, json_file_name="WORK_SHIFT")
#
#     if not correct_data:
#         return
#
#     board_config.current_file = correct_data
#
#     reply_markup = await add_subtract_inline_keyboard_with_action()
#     await call.message.answer(text=correct_data, reply_markup=reply_markup)


async def delete_violation_files_from_pc(message: types.Message, file):
    """Удаление файлов из сервера

    :param message:
    :param file:
    :return:
    """

    # if not await del_file(path=file['json_full_name']):


#         await MyBot.bot.message.answer(text=Messages.Error.file_not_found)
#     await message.answer(text=Messages.Removed.violation_data_pc)
#
#     if not await del_file(path=file['photo_full_name']):
#         await message.answer(text=Messages.Error.file_not_found)
#     await message.answer(text=Messages.Removed.violation_photo_pc)


async def del_file(path) -> bool:
    """Удаление файла из памяти сервера

    :param path:
    :return:
    """
    if os.path.isfile(path):
        try:
            os.remove(path)
            return True
        except os.error as err:
            logger.error(f'{Messages.Error.file_not_found} {repr(err)}')
            return False
    return False


async def delete_violation_files_from_gdrive(message, file, violation_file):
    """Удаление файлов из google drive

    :param violation_file:
    :param file:
    :param message:
    :return:
    """

    if not WRITE_DATA_ON_GOOGLE_DRIVE:
        logger.info(f'{WRITE_DATA_ON_GOOGLE_DRIVE = } abort upload / download from Google Drive')
        return False

    # drive_service = await drive_account_credentials()


#
#     if file.get("violation_id"):
#         name: str = file.get("violation_id")
#     else:
#         name: str = file.get("file_id")
#
#     violation_data_file = violation_file['json_full_name']
#     violation_data_parent_id = violation_file['json_folder_id']
#
#     if not await del_file_from_gdrive(drive_service=drive_service,
#                                       name=name,
#                                       violation_file=violation_data_file,
#                                       parent_id=violation_data_parent_id):
#         await message.answer(text=Messages.Error.file_not_found)
#     await message.answer(text=Messages.Removed.violation_data_gdrive_delete)
#
#     violation_photo_file = violation_file['photo_full_name']
#     violation_photo_parent_id = violation_file['photo_folder_id']
#
#     if not await del_file_from_gdrive(drive_service=drive_service,
#                                       name=name,
#                                       violation_file=violation_photo_file,
#                                       parent_id=violation_photo_parent_id):
#         await message.answer(text=Messages.Error.file_not_found)
#     await message.answer(text=Messages.Removed.violation_photo_gdrive)


async def del_file_from_gdrive(drive_service, *, name, violation_file, parent_id) -> bool:
    """Удаление файлов из google drive

    :param parent_id:
    :param violation_file:
    :param name:
    :param drive_service:
    :return:
    """

    mime_type: str = str(guess_type(violation_file)[0])
    q = await q_request_constructor(name=name,
                                    parent=parent_id,
                                    mime_type=mime_type
                                    )
    params = await params_constructor(q=q, spaces="drive")
    v_files = await find_files_by_params(drive_service, params=params)
    pprint(f"find_files {v_files}")

    for v in v_files:
        if v.get("id"):
            return True if await delete_folder(service=drive_service, folder_id=v["id"]) else False
    return False
