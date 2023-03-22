"""Модуль содержащий класс(-ы) функций периодических проверок по времени"""
import asyncio
from apps.core.checker.check_utils import (periodic_check_data_base,
                                           periodic_check_work)


class PeriodicCheck:
    """Основной класс запуска периодических проверок"""

    __instance = None

    def __new__(cls, val):
        if PeriodicCheck.__instance is None:
            PeriodicCheck.__instance = object.__new__(cls)
        PeriodicCheck.__instance.val = val
        return PeriodicCheck.__instance

    @classmethod
    async def run(cls):
        """Функция запуска проверок"""
        await cls.start_checks()

    @staticmethod
    async def start_checks() -> None:
        """Запуск указанных поверок"""

        task1 = asyncio.create_task(periodic_check_data_base(), name='check_data_base')
        task2 = asyncio.create_task(periodic_check_work(), name='check_work')

        await task1
        await task2
