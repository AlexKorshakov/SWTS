from aiogram import Dispatcher, types
from apps.core.bot.messages.messages import Messages
from loader import logger


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand(command="/start", description="Начало работы"),
            types.BotCommand(command="/developer", description="Разработчик"),
            types.BotCommand(command="/help", description="Вызов справки"),
            types.BotCommand(command="/cancel", description="Отмена всех действий"),
            types.BotCommand(command="/generate", description="Формирование документов"),
            # types.BotCommand(command="/generate_act", description="Формирование акта"),
            # types.BotCommand(command="/generate_report", description="Формирование отчета"),
            # types.BotCommand(command="/generate_stat", description="Формирование статистики"),
            types.BotCommand(command="/correct_entries_handler", description="Изменение данных"),
            types.BotCommand(command="/add_entries", description="Добавление данных"),
            # types.BotCommand(command="/admin_func", description="Админка"),
            # types.BotCommand(command="/send_mail", description="Отправка отчета"),
            # types.BotCommand(command="/test", description="Тестовые команды"),
        ]
    )
    logger.info(Messages.bot_setting_commands)
