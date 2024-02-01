import logging

from aiogram import types, executor
from aiogram import Bot, Dispatcher

API_TOKEN = 'BOT TOKEN HERE'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher



from create_bot.create_bot import bot, dp

bot:Bot = bot
dp:Dispatcher = dp


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler()
async def echo(message: types.Message):

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)