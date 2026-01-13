
import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config

# Configure logging
logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())

