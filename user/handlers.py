from aiogram import types, executor
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext

import asyncio

from create_bot.create_bot import bot, dp

from major.manager import UserManager
from user.states import UserStates

from icecream import ic

bot: Bot = bot
dp: Dispatcher = dp


# @dp.message_handler(commands=["start", "help"])
# async def send_welcome(message: types.Message):
#    manager = UserManager()


@dp.callback_query_handler(lambda call: True, state="*")
async def but_filter(call: types.CallbackQuery, state: FSMContext):
    manager = UserManager(call=call)
    await manager.answer()


@dp.message_handler(state="*")
async def empty(message: types.Message, state: FSMContext):
    # ic(await state.get_state())
    manager = UserManager(msg=message, state=await state.get_state())
    await manager.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
