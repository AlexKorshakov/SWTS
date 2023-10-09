from loader import logger

logger.debug(f"{__name__} start import")

from . import (
    bot_admin_notify,
    check_user_registration,
    # delete_message,
)

logger.debug(f"{__name__} finish import")
