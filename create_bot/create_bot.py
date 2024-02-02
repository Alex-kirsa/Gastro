from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import config
import logging
import asyncio

logging.basicConfig(level=logging.INFO)

loop = asyncio.get_event_loop()

storage = MemoryStorage()

bot: Bot = Bot(token=config.BOT_TOKEN, parse_mode="html", loop=loop)
dp: Dispatcher = Dispatcher(bot, loop=loop, storage=storage)
