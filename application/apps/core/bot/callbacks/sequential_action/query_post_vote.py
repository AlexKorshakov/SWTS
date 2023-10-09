from aiogram.dispatcher import FSMContext

from apps.core.bot.bot_utils.check_user_registration import check_user_access
from loader import logger

logger.debug(f"{__name__} start import")

from aiogram import types
from apps.core.bot.callbacks.sequential_action.correct_headlines_data_answer import \
    get_headlines_text
from apps.core.bot.callbacks.sequential_action.correct_violations_data_answer import \
    get_violations_text
from apps.core.bot.data.board_config import BoardConfig as board_config
from apps.core.bot.callbacks.sequential_action.category import (HEADLINES_DATA_LIST,
                                                                VIOLATIONS_DATA_LIST)
from apps.core.bot.handlers.correct_entries.correct_entries_handler import (
    delete_violation_files_from_gdrive, delete_violation_files_from_pc)
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import (build_inlinekeyboard,
                                                                        posts_cb)
from apps.core.bot.messages.messages import Messages
from apps.core.bot.reports.report_data import headlines_data
from apps.core.utils.generate_report.generate_daily_report.set_daily_report_values import \
    set_report_headlines_data_values
from apps.core.utils.generate_report.get_file_list import get_json_file_list
from apps.core.utils.json_worker.read_json_file import read_json_file
from apps.MyBot import MyBot, bot_send_message
from config.config import SEPARATOR

logger.debug(f"{__name__} finish import")


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['del_current_post']))
async def call_del_current_violation(call: types.CallbackQuery, callback_data: dict[str, str],
                                     state: FSMContext = None):
    """

    :param call:
    :param callback_data:
    :return:
    """
    chat_id = call.message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    v_data: dict = await state.get_data()

    action: str = callback_data['action']

    if action != 'del_current_post':
        return

    # for item in board_config.violation_menu_list:
    for item in v_data['violation_menu_list']:

        try:
            # if board_config.current_file != item:
            if v_data['current_file'] != item:
                continue

            logger.debug(f"{chat_id = }  Выбрано: {item}")
            await call.message.edit_reply_markup()  # удаление клавиатуры
            # for file in board_config.violation_file:
            for file in v_data['violation_file']:

                if file['description'] != item:
                    continue

                violation_file = await read_json_file(file['json_full_name'])

                if not violation_file:
                    await bot_send_message(chat_id=chat_id, text=Messages.Error.file_not_found)
                    continue

                try:
                    logger.info(
                        f"**Find  https://drive.google.com/drive/folders/{violation_file['json_folder_id']}"
                        f" in Google Drive.**")
                    logger.info(
                        f"**Find  https://drive.google.com/drive/folders/{violation_file['photo_folder_id']}"
                        f" in Google Drive.**")
                except KeyError as key_error:
                    logger.error(f"{repr(key_error)}")

                await delete_violation_files_from_pc(call.message, file=file)
                await delete_violation_files_from_gdrive(call.message, file=file, violation_file=violation_file)

                # board_config.current_file = None
                await board_config(state, "current_file", None).set_data()

                break
        except Exception as callback_err:
            logger.error(f"{repr(callback_err)}")
        break


# @MyBot.dp.callback_query_handler(posts_cb.filter(action=['correct_registration_data']))
# async def call_correct_registration_data(call: types.CallbackQuery, callback_data: dict[str, str], state: FSMContext = None):
#     """
#
#     :param call:
#     :param callback_data:
#     :return:
#     """
#     chat_id = call.message.chat.id
#     if not await check_user_access(chat_id=chat_id):
#         return
#     action: str = callback_data['action']
#     registration_text: str = ''
#
#     if action == 'correct_registration_data':
#
#         registration_file_list = await get_registration_json_file_list(chat_id=chat_id)
#
#         if not registration_file_list:
#             registration_file_list = await get_registration_json_file_list(chat_id=chat_id)
#
#         if not registration_file_list:
#             logger.warning(Messages.Error.registration_file_list_not_found)
#             await bot_send_message(chat_id, Messages.Error.file_list_not_found)
#             return
#
#         registration_data: dict = await read_json_file(registration_file_list)
#
#         if not registration_data:
#             logger.error(f"registration_data is empty")
#             await bot_send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
#             return
#
#         if registration_data:
#             registration_text = await get_registration_text(registration_data)
#
#         await bot_send_message(chat_id, text=registration_text)
#
#         menu_level = board_config.menu_level = 1
#         menu_list = board_config.menu_list = REGISTRATION_DATA_LIST
#
#         reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=menu_level, level=1)
#
#         await bot_send_message(text=Messages.Choose.entry, reply_markup=reply_markup)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['correct_commission_composition']))
async def call_correct_commission_composition(call: types.CallbackQuery, callback_data: dict[str, str],
                                              state: FSMContext = None):
    """

    :param call:
    :param callback_data:
    :return:
    """

    chat_id = call.message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    action: str = callback_data['action']
    headlines_text = ''

    if action == 'correct_commission_composition':

        await set_report_headlines_data_values(chat_id=chat_id)

        if headlines_data:
            headlines_text = await get_headlines_text(headlines_data)

    await bot_send_message(chat_id=chat_id, text=headlines_text)

    # menu_level = board_config.menu_level = 1
    # menu_list = board_config.menu_list = HEADLINES_DATA_LIST
    menu_level = await board_config(state, "menu_level", 1).set_data()
    menu_list = await board_config(state, "menu_list", HEADLINES_DATA_LIST).set_data()

    reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=menu_level, level=1)

    await bot_send_message(chat_id=chat_id, text=Messages.Choose.entry, reply_markup=reply_markup)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['correct_current_post']))
async def call_correct_current_post(call: types.CallbackQuery, callback_data: dict[str, str], state: FSMContext = None):
    """

    :param call:
    :param callback_data:
    :return:
    """
    chat_id = call.message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    v_data: dict = await state.get_data()

    action: str = callback_data['action']
    violations_file_path = ''

    if action == 'correct_current_post':

        violations_files_list = await get_json_file_list(chat_id)
        if not violations_files_list:
            logger.warning(Messages.Error.file_list_not_found)
            await bot_send_message(chat_id=chat_id, text=Messages.Error.file_list_not_found)
            return

        violations_id = v_data['current_file'].split(' ')[0]

        for file in violations_files_list:
            if file.split('\\')[-1].split(SEPARATOR)[-1].replace('.json', '') == violations_id:
                violations_file_path = file
                break

        if not violations_file_path:
            logger.warning(f'{Messages.Error.file_not_found} violations_id: {violations_id}')
            await bot_send_message(chat_id=chat_id,
                                   text=f'{Messages.Error.file_not_found} violations_id: {violations_id}')
            return

        violations_data: dict = await read_json_file(file=violations_file_path)

        if violations_data:
            violations_text = await get_violations_text(violations_data)
            await bot_send_message(chat_id=chat_id, text=violations_text)

        # menu_level = board_config.menu_level = 1
        # menu_list = board_config.menu_list = VIOLATIONS_DATA_LIST
        # count_col = board_config.count_col = 2

        menu_level = await board_config(state, "menu_level", 1).set_data()
        menu_list = await board_config(state, "menu_list", VIOLATIONS_DATA_LIST).set_data()
        count_col = await board_config(state, "count_col", 2).set_data()

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=count_col, level=menu_level)

        await bot_send_message(chat_id=chat_id, text=Messages.Choose.entry, reply_markup=reply_markup)


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['correct_abort_current_post']))
async def call_correct_abort_current_post(call: types.CallbackQuery, callback_data: dict[str, str],
                                          state: FSMContext = None):
    """

    :param call:
    :param callback_data:
    :return:
    """

    chat_id = call.message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    action: str = callback_data['action']

    if action == 'correct_abort_current_post':
        await call.message.edit_reply_markup()  # удаление клавиатуры
        # board_config.current_file = None
        # board_config.violation_menu_list: list = []
        # board_config.violation_file: list = []

        await board_config(state, "current_file", None).set_data()
        await board_config(state, "violation_menu_list", []).set_data()
        await board_config(state, "violation_file", []).set_data()
