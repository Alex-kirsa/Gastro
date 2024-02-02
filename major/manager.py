from user.text import UserText
from user.reply_marcups import UserReplyMarkup
from user.states import UserStates
from google_sheets import GoogleSheets

from create_bot import storage


# from user.callbacks import UserCallbackData

from aiogram.dispatcher import FSMContext
from aiogram import types

# from aiogram.dispatcher import FSMContext

import datetime

import asyncio

from icecream import ic


class UserManager:
    _commands_key = {"/start": "start_message", "/help": "start_message"}

    def __init__(
        self,
        msg: types.Message = None,
        call: types.CallbackQuery = None,
        state_name: str = None,
    ):
        self.msg = msg
        self.call = call
        self.states = UserStates(state_name)
        self.text = UserText()
        self.reply_marcup = UserReplyMarkup()

        if self.call:
            source = self.call
        else:
            source = self.msg

        self.memory_state = FSMContext(
            storage, source.from_user.id, source.from_user.id
        )

        self.key_data = None
        if self.states.state_name:
            self.states.state_name = self.states.state_name.split(":")[1]
            self.key_data = self.states.state_name
        elif self.call:
            self.key_data = self.call.data.split(":")[0]
        else:
            self.key_data = UserManager._commands_key.get(msg.text, "empty")
        assert self.key_data is not None

    async def answer(self):
        ic(self.key_data)
        await getattr(self, self.key_data)()

    async def start_message(self):
        await self.msg.answer(await self.text.get_text(self.key_data))
        await asyncio.sleep(0.2)
        await self.empty()

    async def empty(self):
        reply_markup = await self.reply_marcup.get_marcup("choose_option_to_continue")
        await self.msg.answer(
            await self.text.get_text("choose_option_to_continue"),
            reply_markup=reply_markup,
        )

    async def get_recipe(self):
        await self.call.message.delete()
        self.states.state_name = "enter_date"
        await self.call.message.answer(self.text.stock.get(self.states.state_name))
        await getattr(self.states, self.states.state_name).set()

    async def _is_date(self, msg: str) -> bool:
        date = list()
        for sym in msg:
            if not sym.isdigit():
                date = msg.split(sym)
                break
        try:
            if datetime.date(day=int(date[0]), month=int(date[1]), year=int(date[2])):
                return True
        finally:
            return False

    async def enter_date(self):
        if await self._is_date(self.msg.text):
            self.gsheets = GoogleSheets()
            self.memory_state.update_data({"date": self.msg.text})

            if await self.gsheets.time_of_day_are_two(self.msg.text):
                self.key_data = "when_event_happened"
                reply_marcup = await self.reply_marcup.get_marcup(
                    self.key_data, row_width=2
                )
                await self.msg.answer(
                    self.text.get_text(self.key_data),
                    reply_markup=reply_marcup,
                )
            else:
                self.key_data = "food_was_then"
                await self.food_was_then()
        else:
            await self.msg.answer(self.text.get_text(self.states.state_name))

    async def when_event_happened(self):
        self.states.state.update_data({"time_of_day": self.call.data.split(":")[1]})
        self.key_data = "food_was_then"
        await self.msg.answer(self.text.get_text(self.key_data))

    async def food_was_then(self):
        data: dict = await self.memory_state.get_data()
        time_of_day = None
        if "time_of_day" in data:
            time_of_day = data.get("time_of_day")

        all_text = await self.gsheets.get_dishes(data.get("date"), time_of_day)

        text = []

        ic(all_text)
        for el in all_text:
            text.append(
                '<a href="{url}">{text}</a>'.format(
                    url=el.get("url"), text=el.get("text")
                )
            )

        text = "\n".join(text)

        await self.msg.answer(self.text.stock.get(self.key_data).format(text))

    async def send_booking_req(self):
        await self.call.message.answer(
            await self.text.get_text(self.key_data),
            reply_markup=await self.reply_marcup.get_marcup(self.key_data),
        )

    async def change_form(self):
        cb_data = self.call.data.split(":")
        cb_data
        if len(cb_data) > 1:
            await self.call.message.delete()
            await asyncio.sleep(0.1)
            send_text_dict: dict = self.text._stock["change_form_state"]
            await self.call.message.answer(send_text_dict.get(cb_data[1]))
            await self.memory_state.set_state(self.states.change_form_state)
            data = await self.memory_state.get_data()
            data.update({"change_form_state": cb_data[1]})
            await self.memory_state.update_data(**data)
            return
        await self.call.message.delete()
        await asyncio.sleep(0.2)
        await self.send_change_form_message(source=self.call.message)

    async def send_change_form_message(self, source):
        data = await self.memory_state.get_data()
        ic(data)
        dic = dict()
        self.cou = 0
        for el in self.reply_marcup.MESSAGES.get("change_form"):
            dg = data.get(el, await self._cou_change_form())
            dic.update({f"{el}": dg})

        await source.answer(
            await self.text.get_text(
                key="change_form",
                **dic,
            ),
            reply_markup=await self.reply_marcup.get_marcup("change_form"),
        )

    async def _cou_change_form(self):
        self.cou += 1
        return ""

    async def change_form_state(self):
        data = await self.memory_state.get_data()
        change_form_state = data.get("change_form_state", None)

        if change_form_state == "desired_date" and not self._is_date(self.msg.text):
            await self.msg.answer(
                await self.text["change_form_states"].get(change_form_state)
            )
        else:
            await self.memory_state.update_data({change_form_state: self.msg.text})
            await asyncio.sleep(0.1)
            await self.send_change_form_message(source=self.msg)
            await self.memory_state.finish()

            if self.cou == 0:
                self.key_data = "should_we_send_form"
                asyncio.sleep(0.1)
                await self.msg.answer(
                    await self.text.get_text(key=self.key_data),
                    reply_markup=await self.reply_marcup.get_marcup(key=self.key_data),
                )

    async def should_we_send_form(self):
        self.key_data = "should_we_send_form"
        await self.call.message.edit_text(self.text.get_text(self.key_data))
        await self.call.message.edit_reply_markup(None)
