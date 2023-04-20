"""Модуль содержащий класс(-ы) функций периодических проверок по времени"""
import asyncio

from apps.core.checker.periodic_check_work import periodic_check_work
from apps.core.checker.periodic_check_data_base import periodic_check_data_base
from apps.core.checker.periodic_check_unclosed_points import periodic_check_unclosed_points


class PeriodicCheck:
    """Основной класс запуска периодических проверок"""

    __instance = None

    def __new__(cls, val):
        if PeriodicCheck.__instance is None:
            PeriodicCheck.__instance = object.__new__(cls)
        PeriodicCheck.__instance.val = val
        return PeriodicCheck.__instance

    def __repr__(self):
        """"""
        return str(self)

    @classmethod
    async def run(cls):
        """Функция запуска проверок"""
        await cls.start_checks()

    @staticmethod
    async def start_checks() -> None:
        """Запуск указанных поверок"""

        # await asyncio.gather(periodic_check_data_base(), periodic_check_work(),periodic_check_unclosed_points())
        # check_data_base_task = asyncio.create_task(periodic_check_data_base(), name='check_data_base')
        # check_work_task = asyncio.create_task(periodic_check_work(), name='check_work')
        # check_unclosed_points_task = asyncio.create_task(periodic_check_unclosed_points(), name='check_unclosed_points')

        check_data_base_task = asyncio.gather(periodic_check_data_base())
        check_work_task = asyncio.gather(periodic_check_work())
        check_unclosed_points_task = asyncio.gather(periodic_check_unclosed_points())

        await check_data_base_task
        await check_work_task
        await check_unclosed_points_task
