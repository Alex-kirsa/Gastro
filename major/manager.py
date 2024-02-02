from user.text import UserText
from user.reply_marcups import UserReplyMarkup
from user.states import UserStates
from user.callbacks import UserCallbackData

from aiogram import types
from aiogram.dispatcher import FSMContext

import asyncio

from icecream import ic


class UserManager:
    _commands_key = {"/start": "start_message", "/help": "start_message"}

    def __init__(
        self,
        msg: types.Message = None,
        call: types.CallbackQuery = None,
        state: FSMContext = None,
    ):
        self.msg = msg
        self.call = UserCallbackData()
        self.state = UserStates()
        self.text = UserText()
        self.reply_marcup = UserReplyMarkup()
        # self.func_mapping = UserManager._func_mapping

        self.key_data = None
        if state:
            self.key_data = str(state)
        elif call:
            self.key_data = call.callback_data
        else:
            self.key_data = UserManager._commands_key.get(msg.text, "empty")
        assert self.key_data is not None

    async def answer(self):
        await getattr(self, self.key_data)()

    async def start_message(self):
        await self.msg.answer(self.text.stock.get("start_message"))
        await asyncio.sleep(0.2)
        await self.empty()

    async def empty(self):
        reply_markup = await self.reply_marcup.get_marcup("choose_option_to_continue")
        await self.msg.answer(
            self.text.stock.get("choose_option_to_continue"),
            reply_markup=reply_markup,
        )

    _func_mapping = {"start_message": start_message, "empty": empty}
