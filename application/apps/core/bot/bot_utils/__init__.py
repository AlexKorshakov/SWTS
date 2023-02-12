from loader import logger

logger.debug(f"{__name__} start import")

from . import (
    bot_admin_notify,
    check_user_registration,
    # delete_message,
    # notify_admins,
    # select_start_category,
    # set_bot_commands,
)

logger.debug(f"{__name__} finish import")
