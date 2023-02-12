from loader import logger

logger.debug(f"{__name__} start import")

from . import generate_daily_report

logger.debug(f"{__name__} finish import")