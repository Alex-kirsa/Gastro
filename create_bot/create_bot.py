from aiogram import Bot, Dispatcher
import config
import logging

logging.basicConfig(level=logging.INFO)

bot: Bot = Bot(token=config.BOT_TOKEN, parse_mode="html")
dp: Dispatcher = Dispatcher(bot)
