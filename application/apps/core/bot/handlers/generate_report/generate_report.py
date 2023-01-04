from aiogram import types
from aiogram.dispatcher.filters import Command

from apps.MyBot import MyBot
from apps.core.utils.reports_processor.report_worker import create_and_send_report
from apps.core.utils.generate_report.generate_daily_report.create_and_send_daily_report import \
    create_and_send_daily_report
from loader import logger

from apps.core.bot.messages.messages import Messages
from apps.core.utils.misc import rate_limit

from apps.core.bot.bot_utils.check_user_registration import check_user_access


@rate_limit(limit=10)
@MyBot.dp.message_handler(Command('generate'))
async def generate(message: types.Message) -> None:
    """Формирование и отправка отчета пользователю
    :param message:
    :return: None
    """
    chat_id = message.chat.id
    if not await check_user_access(chat_id=chat_id):
        return

    await message.answer(f'{Messages.Report.start} \n'
                         f'{Messages.wait}')

    logger.info(f'User @{message.from_user.username}:{chat_id} generate mip report')
    if await create_and_send_daily_report(chat_id=chat_id):
        logger.info(Messages.Report.generated_successfully)

    logger.info(f'User @{message.from_user.username}:{chat_id} generate report')
    if await create_and_send_report(chat_id=chat_id):
        logger.info(Messages.Report.generated_successfully)
