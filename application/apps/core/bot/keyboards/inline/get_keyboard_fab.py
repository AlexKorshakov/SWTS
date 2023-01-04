from aiogram import types
from aiogram.types import InlineKeyboardMarkup

from apps.core.bot.callbacks.callback_action import cb_start


async def get_keyboard_fab() -> InlineKeyboardMarkup:
    """Действия при начале регистрации нарушений (в конце ввода данных).
    Возвращает кнопки 'Зарегистрировать' и 'Отмена'
    """
    buttons = [
        types.InlineKeyboardButton(text="Зарегистрировать", callback_data=cb_start.new(action="start_registration")),
        types.InlineKeyboardButton(text="Отмена", callback_data=cb_start.new(action="abort_registration"))
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    return keyboard
