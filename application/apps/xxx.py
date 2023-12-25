from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from AiogramStorages.storages import SQLiteStorage

from config.config import BOT_TOKEN, Udocan_HSE_user_base_storage

assistant = Bot(token=BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
# storage = SQLiteStorage(db_path=Udocan_HSE_user_base_storage)

dp_assistant = Dispatcher(bot=assistant, storage=storage)
