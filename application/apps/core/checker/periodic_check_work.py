import asyncio

from apps.core.checker.check_utils import get_now, PERIOD
from loader import logger


async def periodic_check_work():
    """Периодическое напоминание о работе"""
    # print(f'create_qr_code periodic_check_work')
    while True:
        await asyncio.sleep(1)
        logger.info(f"i'm work ::: {await get_now()}")
        # print(f"i'm work ::: {now}")
        await asyncio.sleep(PERIOD)
