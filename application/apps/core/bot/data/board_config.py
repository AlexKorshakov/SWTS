from __future__ import annotations

from aiogram.dispatcher import FSMContext


class BoardConfig:
    """Класс для действий над состоянием state"""

    def __init__(self, state: FSMContext = None, atr_name: str = None, art_val: any = None):
        self.state: FSMContext = state
        self.atr_name: str = atr_name
        self.art_val: any = art_val

    async def set_data(self, atr_name: str = None, art_val: any = None) -> any:
        """Присвоение значений состоянию self.state. Возвращает значение атрибута art_val

        :param atr_name: str - имя атрибута
        :param art_val: any значение атрибута
        :return: art_val
        """
        atr_name: str = atr_name if atr_name else self.atr_name
        art_val: any = art_val if art_val else self.art_val

        if art_val is None:
            return self.state

        await self.state.update_data({atr_name: art_val})

        return art_val

    async def get_data(self) -> dict:
        """Получение данных состояния self.state

        :return: dict
        """
        v_data: dict = await self.state.get_data()
        return v_data
