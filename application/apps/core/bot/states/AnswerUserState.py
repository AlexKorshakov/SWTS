from aiogram.dispatcher.filters.state import State, StatesGroup


class AnswerUserState(StatesGroup):
    # ответ пользователя Описание
    description = State()
    # ответ пользователя Состояние
    comment = State()

    location = State()
