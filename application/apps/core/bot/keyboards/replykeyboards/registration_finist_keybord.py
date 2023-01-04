from aiogram import types
from aiogram.types import ReplyKeyboardMarkup


async def registration_finish_keyboard() -> ReplyKeyboardMarkup:
    """Сборка клавиатуры команд в конце ввода данных
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Завершить регистрацию"]

    keyboard.add(*buttons)

    return keyboard
