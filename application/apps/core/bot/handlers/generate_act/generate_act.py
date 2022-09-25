from aiogram import types
from aiogram.dispatcher.filters import Command

from app import MyBot
from apps.core.bot.messages.messages import Messages
from apps.core.bot.utils.misc import rate_limit
from apps.core.bot.utils.report_worker import create_and_send_act_prescription
from apps.core.bot.utils.secondary_functions.check_user_registration import check_user_access
from loader import logger


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('generate_act'))
async def act_generate_handler(message: types.Message) -> None:
    """Запуск генерации акта - предписания
    :param message:
    :return:
    """

    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    await message.answer(f'{Messages.Report.start_act} \n'
                         f'{Messages.wait}')

    logger.info(f'User @{message.from_user.username}:{chat_id} generate act prescription')
    if await create_and_send_act_prescription(chat_id=chat_id):
        logger.info(Messages.Report.acts_generated_successfully)
