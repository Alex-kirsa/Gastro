from aiogram import types, executor
from aiogram import Bot, Dispatcher

import asyncio

from create_bot.create_bot import bot, dp

from major.manager import UserManager

from icecream import ic

bot: Bot = bot
dp: Dispatcher = dp


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    manager = UserManager(message.from_user.id)
    await message.answer(manager.text.stock.get("start_message"))
    await asyncio.sleep(0.1)
    await empty(message)


@dp.message_handler()
async def empty(message: types.Message):
    manager = UserManager(message.from_user.id)
    reply_markup = await manager.reply_markup.get_marcup("choose_option_to_continue")
    await message.answer(
        manager.text.stock.get("choose_option_to_continue"),
        reply_markup=reply_markup,
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
