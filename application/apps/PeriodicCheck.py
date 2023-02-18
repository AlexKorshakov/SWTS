import asyncio
from apps.core.checker.check_utils import (periodic_check_data_base,
                                           periodic_check_work)
import heartrate
heartrate.trace(browser=True)


class PeriodicCheck:

    @classmethod
    def run(cls):

        asyncio.run(cls.start_checks())

    @staticmethod
    async def start_checks() -> None:
        print(f'PeriodicCheck.start_checks')
        task1 = asyncio.create_task(periodic_check_data_base())
        task2 = asyncio.create_task(periodic_check_work())

        await task1
        await task2
