from aiogram import Bot, Dispatcher


#sys.path.append("..")
import config
bot:Bot = Bot(token=config.BOT_TOKEN)
dp:Dispatcher = Dispatcher(bot)









