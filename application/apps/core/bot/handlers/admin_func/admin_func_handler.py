from __future__ import annotations

from aiogram.dispatcher import FSMContext

from loader import logger

logger.debug(f"{__name__} start import")
import time

from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from apps.core.bot.bot_utils.bot_admin_notify import admin_notify
from apps.core.bot.bot_utils.check_user_registration import check_user_access
from apps.core.bot.data.board_config import BoardConfig as board_config
from apps.core.bot.callbacks.sequential_action.category import ADMIN_MENU_LIST
from apps.core.bot.filters.custom_filters import is_private
from apps.core.bot.keyboards.inline.build_castom_inlinekeyboard import \
    build_inlinekeyboard, posts_cb
from apps.core.bot.messages.messages_test import msg
from apps.core.checker.periodic_check_indefinite_normative import check_indefinite_normative
from apps.core.checker.periodic_check_unclosed_points import check_acts_prescriptions_status
from apps.core.checker.periodic_check_unclosed_points_for_subcontractor import \
    check_acts_prescriptions_status_for_subcontractor
from apps.core.settyngs import get_sett
from apps.core.bot.messages.messages import Messages
from apps.core.utils.misc import rate_limit
from apps.core.utils.secondary_functions.get_json_files import get_registered_users
from apps.MyBot import MyBot, bot_send_message
from config.config import ADMIN_ID, DEVELOPER_ID

logger.debug(f"{__name__} finish import")


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('admin_func'))
async def admin_func_handler(message: types.Message, state: FSMContext = None):
    """Административные функции

    :param message:
    :return: None
    """

    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        logger.error(f'access fail {chat_id = }')
        return

    if not get_sett(cat='enable_features', param='use_catalog_func').get_set():
        msg_text: str = f"{await msg(chat_id, cat='error', msge='features_disabled', default=Messages.Error.features_disabled).g_mas()}"
        await bot_send_message(chat_id=chat_id, text=msg_text, disable_web_page_preview=True)
        return

    # TODO  переделать
    if chat_id != int(ADMIN_ID) or chat_id != int(DEVELOPER_ID):
        await admin_notify(
            user_id=chat_id, notify_text=f'User @{message.from_user.username}:{chat_id} попытка доступа в админку!'
        )
        text: str = 'У Вас нет прав доступа к административным функциям!\n' \
                    'По всем вопросам обращайтесь к администратору\n' \
                    'https://t.me/AlexKor_MSK'

        await bot_send_message(chat_id=chat_id, text=text, disable_web_page_preview=True)
        return

    reply_markup = await add_correct_inline_keyboard_with_action()
    text: str = 'Выберите действие'

    await bot_send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)


async def add_correct_inline_keyboard_with_action():
    """Формирование сообщения с текстом и кнопками действий в зависимости от параметров

    :return:
    """

    markup = types.InlineKeyboardMarkup()

    markup.add(types.InlineKeyboardButton(
        'Проверить статус Актов',
        callback_data=posts_cb.new(id='-', action='check_acts_prescriptions_status'))
    )
    markup.add(types.InlineKeyboardButton(
        'Отправить статус Актов подрядчикам',
        callback_data=posts_cb.new(id='-', action='check_acts_prescriptions_status_for_subcontractor'))
    )
    markup.add(types.InlineKeyboardButton(
        'Проверить нормативку',
        callback_data=posts_cb.new(id='-', action='check_indefinite_normative'))
    )

    return markup


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['check_acts_prescriptions_status']))
async def check_acts_prescriptions_status_answer(
        call: types.CallbackQuery, callback_data: dict[str, str], state: FSMContext = None):
    """

    :return:
    """
    hse_user_id = call.message.chat.id
    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    msg_text = await msg(hse_user_id, cat='error', msge='error_action', default=Messages.Error.error_action).g_mas()
    await bot_send_message(chat_id=hse_user_id, text=msg_text)
    await check_acts_prescriptions_status()


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['check_acts_prescriptions_status_for_subcontractor']))
async def check_acts_prescriptions_status_for_subcontractor_answer(
        call: types.CallbackQuery, callback_data: dict[str, str], state: FSMContext = None):
    """

    :return:
    """
    hse_user_id = call.message.chat.id
    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    # msg_text = await msg(hse_user_id, cat='error', msge='error_action', default=Messages.Error.error_action).g_mas()
    # await bot_send_message(chat_id=hse_user_id, text=msg_text)
    await check_acts_prescriptions_status_for_subcontractor()
    await bot_send_message(chat_id=hse_user_id, text="Уведомления направлены")


@MyBot.dp.callback_query_handler(posts_cb.filter(action=['check_indefinite_normative']))
async def check_indefinite_normative_answer(
        call: types.CallbackQuery, callback_data: dict[str, str], state: FSMContext = None):
    """

    :return:
    """
    hse_user_id = call.message.chat.id
    if not await check_user_access(chat_id=hse_user_id):
        logger.error(f'access fail {hse_user_id = }')
        return

    msg_text = await msg(hse_user_id, cat='error', msge='error_action', default=Messages.Error.error_action).g_mas()
    await bot_send_message(chat_id=hse_user_id, text=msg_text)
    await check_indefinite_normative()


@MyBot.dp.callback_query_handler(is_private, lambda call: call.data in ADMIN_MENU_LIST)
async def admin_function_answer(call: types.CallbackQuery, user_id: int | str = None, state: FSMContext = None):
    """Обработка ответов содержащихся в ADMIN_MENU_LIST
    """
    hse_user_id = call.message.chat.id if call else user_id

    users_datas, users_ids = await get_registered_users()

    if call.data == 'Показать всех пользователей':
        # menu_level = board_config.menu_level = 2
        # menu_list = board_config.menu_list = users_datas

        menu_level = await board_config(state, "menu_level", 2).set_data()
        menu_list = await board_config(state, "menu_list", users_datas).set_data()

        reply_markup = await build_inlinekeyboard(some_list=menu_list, num_col=1, level=menu_level)
        await bot_send_message(chat_id=hse_user_id, text=Messages.Admin.answer, reply_markup=reply_markup)

    if call.data == 'Оповещение':

        text: str = 'Приветствую! \n' \
                    'Бот MIP_HSE_BOT обновился!\n' \
                    '\n' \
                    'Команда: Изменение данных или /correct_entries_handler\n' \
                    'добавлено: \n' \
                    'коррекция данных регистрации \n' \
                    'возможно исправить \n' \
                    '    ФИО\n' \
                    '    Должность\n' \
                    '    Площалку\n' \
                    '    Смена\n' \
                    '    Телефон\n' \
                    '\n' \
                    'коррекция данных зарегистрированных нарушений\n' \
                    'возможно исправить \n' \
                    '    Описание нарушения\n' \
                    '    Комментарий к нарушению\n' \
                    '    Основное направление\n' \
                    '    Количество дней на устранение\n' \
                    '    Степень опасности ситуации\n' \
                    '    Требуется ли оформление акта?\n' \
                    '    Подрядная организация\n' \
                    '    Категория нарушения\n' \
                    '    Уровень происшествия\n' \
                    '\n' \
                    'коррекция данных заголовков отчета (Состав комиссии)\n' \
                    'возможно исправить \n' \
                    '    Руководитель строительства\n' \
                    '    Инженер СК\n' \
                    '    Подрядчик\n' \
                    '    Субподрядчик\n' \
                    '    Вид обхода\n' \
                    '    Представитель подрядчика\n' \
                    '    Представитель субподрядчика\n' \
                    '\n' \
                    'где возможно - добавлен выбор данных из списка\n' \
                    'в остальных случаях - ручной ввод\n' \
                    '\n' \
                    'команда отмены или /cansel прекращает все действия во всех процессах бота\n' \
                    'работает из любого места или меню\n' \
                    '\n' \
                    'исправлены ошибки повышена стабильность работы\n' \
                    '\n' \
                    'По всем вопросам - к разработчику\n' \
                    f'{Messages.help_message}'

        for user_id in users_ids:
            if user_id == ADMIN_ID: continue

            reply_markup = InlineKeyboardMarkup()
            reply_markup.add(
                InlineKeyboardButton(text='написать разработчику', url=f"tg://user?id={ADMIN_ID}")
            )

            try:

                await bot_send_message(chat_id=user_id, text=text, reply_markup=reply_markup)
            except Exception as err:
                logger.error(f'bot.send_message error {repr(err)}')
                await bot_send_message(chat_id=ADMIN_ID, text='bot.send_message error user_id')
                continue

            await admin_notify(
                user_id=user_id,
                notify_text=f'Оповещение отправлено {user_id}'
            )
            time.sleep(1)
