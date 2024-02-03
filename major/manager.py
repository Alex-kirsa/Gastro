from user.text import UserText
from user.reply_marcups import UserReplyMarkup
from user.states import UserStates
from google_sheets import GoogleSheets

from config.settings import CHANNEL_ID, MANAGER_PHONE_NUMBER, ADMINS_LIST
from create_bot import storage, bot


# from user.callbacks import UserCallbackData

from aiogram.dispatcher import FSMContext
from aiogram import types

from database import Database

# from aiogram.dispatcher import FSMContext

import datetime

import asyncio

from icecream import ic


class UserManager:
    _commands_key = {
        "/start": "start_message",
        "/help": "start_message",
        "/admin": "admin_menu",
    }

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
        self.db = Database()

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
        self.db.check_user_in_db(self.msg.from_user.id)
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
        self.key_data = "enter_date"
        await self.call.message.answer(await self.text.get_text(self.key_data))
        await getattr(self.states, self.key_data).set()

    async def _is_date(self, msg: str) -> bool:
        date = list()
        for sym in msg:
            if not sym.isdigit():
                date = msg.split(sym)
                break
        # ic("ASD")
        # try:
        if datetime.date(day=int(date[0]), month=int(date[1]), year=int(date[2])):
            return True
        # finally:
        #    return False

    async def enter_date(self):
        # ic(self.msg.text)
        if await self._is_date(self.msg.text):
            self.gsheets = GoogleSheets()
            await self.memory_state.update_data({"date": self.msg.text})

            if await self.gsheets.time_of_day_are_two(self.msg.text):
                self.key_data = "when_event_happened"
                reply_marcup = await self.reply_marcup.get_marcup(
                    self.key_data, row_width=2
                )
                await self.msg.answer(
                    await self.text.get_text(self.key_data),
                    reply_markup=reply_marcup,
                )
            else:
                self.key_data = "food_was_then"
                await self.food_was_then()
        else:
            await self.msg.answer(await self.text.get_text(self.states.state_name))

    async def when_event_happened(self):
        await self.states.state.update_data(
            {"time_of_day": self.call.data.split(":")[1]}
        )
        self.key_data = "food_was_then"
        await self.food_was_then()
        # await self.msg.answer(self.text.get_text(self.key_data))

    async def food_was_then(self):
        data: dict = await self.memory_state.get_data()
        time_of_day = None
        if "time_of_day" in data:
            time_of_day = data.get("time_of_day")

        all_text = await self.gsheets.get_dishes(data.get("date"), time_of_day)
        assert all_text is not None

        food = []

        # ic(all_text)

        for el in all_text:
            # ic(el, el.get("url"), el.get("name"))
            food.append(
                '<a href="{url}">{text}</a>'.format(
                    url=el.get("url"), text=el.get("name")
                )
            )
        food = "\n".join(food)

        # ic(text, type(text))
        await self.msg.answer(await self.text.get_text("food_was_then", food=food))

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
        await self.call.message.answer(**self._send_change_form_message())

    async def _send_change_form_message(self, source):
        data = await self.memory_state.get_data()
        # ic(data)
        dic = dict()
        self.cou = 0
        for el in self.reply_marcup.MESSAGES.get("change_form"):
            dg = data.get(el, await self._cou_change_form())
            dic.update({f"{el}": dg})

        return {
            "text": self.text.get_text(
                key="change_form",
                **dic,
            ),
            "reply_markup": await self.reply_marcup.get_marcup("change_form"),
        }

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
            await asyncio.sleep(0.2)
            await self.msg.answer(**self._send_change_form_message())
            await self.memory_state.finish()

            if self.cou == 0:
                self.key_data = "should_we_send_form"
                await asyncio.sleep(0.2)
                await self.msg.answer(
                    await self.text.get_text(key=self.key_data),
                    reply_markup=await self.reply_marcup.get_marcup(key=self.key_data),
                )
                await self.memory_state.update_data(
                    {
                        "book_message": {
                            "message_id": self.msg.message_id,
                            "from_chat_id": self.msg.chat.id,
                        }
                    }
                )

    async def leave_review(self):
        await self.call.message.answer(await self.text.get_text("send_me_comment"))
        await self.states.send_me_comment_message.set()

    async def send_me_comment_message(self):
        await self.memory_state.finish()
        await self.msg.copy_to(CHANNEL_ID)
        await asyncio.sleep(0.2)
        await self.msg.answer(await self.text.get_text("message_sent"))
        for u in ADMINS_LIST:
            await bot.send_message(u, await self.text.get_text("new_comment"))
            await self.msg.send_copy(u)

    async def should_we_send_form(self):
        self.key_data = "should_we_send_form"
        data = self.memory_state.get_data()
        for a in ADMINS_LIST:
            await bot.copy_message(a, **data.get("book_message"))

        await self.call.message.edit_text(self.text.get_text(self.key_data))
        await self.call.message.edit_reply_markup(None)

    async def contact_manager(self):
        await bot.send_contact(
            self.call.from_user.id,
            phone_number=MANAGER_PHONE_NUMBER,
            first_name="Менеджер",
        )

    async def view_latest_studio_news(self):
        mailings = self.db.get_all_mailings()

        if len(mailings) == 0:
            await self.call.message.answer(await self.text.get_text("no_mailing"))
        else:
            await bot.copy_message(
                chat_id=self.call.from_user.id,
                from_chat_id=mailings[-1][1],
                message_id=mailings[-1][0],
            )

    async def admin_menu(self):
        if self.msg.from_user.id in ADMINS_LIST:
            await self.msg.answer(
                self.text.get_text("admin_menu"),
                reply_markup=self.reply_marcup.get_marcup("admin_menu"),
            )
        else:
            await self.empty()

    async def mail_to_all_users(self):
        await self.memory_state.set_state(self.states.admin_send_post)
        await self.call.message.answer(self.text.get_text("send_post"))

    async def admin_send_post(self):
        await self.memory_state.finish()
        users_id = self.db.get_all_users()
        cou = 0
        for u in users_id:
            await self.msg.copy_to(u)
            cou += 1
        await self.msg.answer(self.text.get_text("admin_post_sent", cou=cou))
