from __future__ import annotations

from aiogram.dispatcher import FSMContext


class BoardConfig:

    def __init__(self, state: FSMContext = None, atr_name: str = None, art_val: int | str | list | dict | bool = None):
        self.state = state
        self.atr_name = atr_name
        self.art_val = art_val

    async def set_data(self, atr_name=None, art_val=None):
        """

        :return:
        """

        atr_name = atr_name if atr_name else self.atr_name
        art_val: int | str | list | dict | None | bool = art_val if art_val else self.art_val

        if art_val is not None:
            await self.state.update_data({atr_name: art_val})
            return art_val

    async def get_data(self):
        """

        :return:
        """
        v_data: dict = await self.state.get_data()
        return v_data
