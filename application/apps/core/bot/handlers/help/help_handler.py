from loader import logger

logger.debug(f"{__name__} start import")
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import text
from apps.core.bot.keyboards.inline.help_inlinekeyboard import \
    help_inline_button
from apps.core.utils.misc import rate_limit
from apps.MyBot import MyBot, bot_send_message

logger.debug(f"{__name__} finish import")


@rate_limit(limit=5)
@MyBot.dp.message_handler(Command('help'))
async def process_help_command(message: types.Message):
    """Обработка команды help
    """
    help_message = text(
        "Справка по командам\n",
        "/developer - написать разработчику",
        "/cancel- Отмена всех действий",
        "/generate - Формирование документов",
        "/start - Начало работы",
        "/correct_entries - Корректировка введённых значений",
        "/admin_func - Админка",
        "\nВидео инструкция по работе бота",
        sep="\n"
    )

    answer_text = f"{msg(hse_id, cat='help', msge='developer', default='Меня создал').get_msg_async()} https://t.me/AlexKor_MSK"
    await bot_send_message(chat_id=hse_id, text=answer_text)
    await bot_send_message(chat_id=hse_id, text=help_message, reply_markup=await help_inline_button(hse_id=hse_id))
