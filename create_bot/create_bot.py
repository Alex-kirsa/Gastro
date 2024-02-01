from aiogram import Bot, Dispatcher


# sys.path.append("..")
import config

bot: Bot = Bot(token=config.BOT_TOKEN, parse_mode="html")
dp: Dispatcher = Dispatcher(bot)
