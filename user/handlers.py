from aiogram import types, executor
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext

# import asyncio

from create_bot.create_bot import bot, dp

from major.manager import UserManager

# from user.states import UserStates

# from icecream import ic

bot: Bot = bot
dp: Dispatcher = dp


@dp.callback_query_handler(chat_type="private")
async def callback_query_handler(call: types.CallbackQuery):
    manager = UserManager(call=call)
    await manager.answer()


@dp.message_handler(state="*", chat_type="private")
async def message_handler(message: types.Message, state: FSMContext):
    # ic(await state.get_state())
    manager = UserManager(msg=message, state_name=await state.get_state())
    await manager.answer()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
