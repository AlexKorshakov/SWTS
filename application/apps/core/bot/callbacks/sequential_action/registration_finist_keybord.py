from aiogram import types
from aiogram.types import ReplyKeyboardMarkup


async def registration_finish_keyboard() -> ReplyKeyboardMarkup:
    """Сборка клавиатуры команд в конце ввода данных
    """

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    markup.add(
        types.KeyboardButton(
            text="Завершить регистрацию",
        )
    )

    return markup
