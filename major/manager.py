from user.text import UserText
from user.reply_marcups import UserReplyMarkup
from user.states import UserStates
from google_sheets import gs

from config.settings import CHANNEL_ID, MANAGER_USERNAME, ADMINS_LIST
from create_bot import storage, bot


# from user.callbacks import UserCallbackData

from aiogram.dispatcher import FSMContext
from aiogram import types

from database import Database

# from aiogram.dispatcher import FSMContext

import datetime

import asyncio

# from icecream import ic


class UserManager:
    _commands_key = {
        "/start": "start_message",
        "/help": "start_message",
        "/admin": "admin_menu",
        "/menu": "empty",
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
        if self.msg:
            if self.msg.text in UserManager._commands_key:
                self.key_data = UserManager._commands_key.get(msg.text)
            elif self.states.state_name is not None:
                self.states.state_name = self.states.state_name.split(":")[1]
                self.key_data = self.states.state_name
        elif self.call:
            self.key_data = self.call.data.split(":")[0]
        if self.key_data is None:
            self.key_data = "empty"
        assert self.key_data is not None

    async def answer(self):
        # ic(self.key_data)
        await getattr(self, self.key_data)()

    async def start_message(self):
        await self.memory_state.finish()
        await self.msg.answer(await self.text.get_text(self.key_data))
        await asyncio.sleep(0.2)
        await self.empty()

    async def empty(self):
        reply_markup = await self.reply_marcup.get_marcup("choose_option_to_continue")
        text = await self.text.get_text("choose_option_to_continue")
        try:
            await self.msg.answer(
                text,
                reply_markup=reply_markup,
            )
        except:  # noqa: E722
            await self.call.message.answer(
                text,
                reply_markup=reply_markup,
            )

    async def get_recipe(self):
        await self.call.message.delete()
        self.key_data = "enter_date"
        await self.call.message.answer(await self.text.get_text(self.key_data))
        await self.memory_state.set_state(self.states.enter_date)
        # await getattr(self.states, self.key_data).set()

    async def _is_date(self, msg: str) -> bool:
        date = list()
        for sym in msg:
            if not sym.isdigit():
                date = msg.split(sym)
                break
            # ic("ASD")
        try:
            if (
                datetime.date(day=int(date[0]), month=int(date[1]), year=int(date[2]))
                and len(date) == 3
            ):
                self.msg.text = ".".join(date)
                return True
        except:  # noqa: E722
            return False

    async def enter_date(self):
        # ic(self.msg.text)
        if await self._is_date(self.msg.text):
            await self.memory_state.finish()

            await self.memory_state.update_data({"date": self.msg.text})

            if await gs.time_of_day_are_two(self.msg.text):
                self.key_data = "when_event_happened"
                reply_marcup = await self.reply_marcup.get_marcup(
                    key=self.key_data, row_width=2
                )
                await self.msg.answer(
                    await self.text.get_text(self.key_data),
                    reply_markup=reply_marcup,
                )
            else:
                await self.msg.answer(await self.text.get_text("wait_food"))
                self.key_data = "food_was_then"
                await self.food_was_then()
        else:
            await self.msg.answer(await self.text.get_text(self.key_data))

    async def when_event_happened(self):

        await self.call.message.delete()
        await self.memory_state.update_data(
            {"time_of_day": self.call.data.split(":")[1]}
        )
        self.key_data = "food_was_then"
        # self.gsheets = GoogleSheets()
        await self.food_was_then()
        # await self.msg.answer(self.text.get_text(self.key_data))

    async def food_was_then(self):
        data: dict = await self.memory_state.get_data()
        # ic(data)
        time_of_day = None
        if "time_of_day" in data:
            time_of_day = data.get("time_of_day")

        all_text = await gs.get_dishes(data.get("date"), time_of_day)
        assert all_text is not None

        if all_text == []:
            if self.msg:
                await self.msg.answer(await self.text.get_text("no_food"))
            else:
                await self.call.message.answer(await self.text.get_text("no_food"))
            await self.empty()
            return

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
        if self.call:
            source = self.call.message
        else:
            source = self.msg

        await source.answer(await self.text.get_text("food_was_then", food=food))
        await asyncio.sleep(3)
        await self.empty()

    async def send_booking_req(self):
        await self.call.message.answer(
            await self.text.get_text(self.key_data),
            reply_markup=await self.reply_marcup.get_marcup(self.key_data),
        )

    async def change_form(self):
        cb_data = self.call.data.split(":")
        # cb_data
        # ic(cb_data)
        await self.call.message.delete()
        send_text_dict: dict = self.text._stock["change_form_state"]
        await self.memory_state.set_state(self.states.change_form_state)
        if len(cb_data) > 1:
            # await asyncio.sleep(0.1)
            state = cb_data[1]
            # data = await self.memory_state.get_data()
            # ic(data)
            # data.update({"change_form_state": cb_data[1]})
        else:
            state = list(self.text._stock["change_form_state"])[0]
            # ic(state)
        await self.memory_state.update_data({"change_form_state": state})
        await self.call.message.answer(send_text_dict.get(state))
        # await self.call.message.delete()
        # await asyncio.sleep(0.2)
        # await self.call.message.answer(**await self._send_change_form_message())

    async def _send_change_form_message(self):
        form_data = await self.memory_state.get_data()
        form_data: dict = form_data.get("form_data")
        # ic(data)
        # dic = dict()
        # self.cou = 0
        # all_form_kwargs = self.text._stock.get("change_form_state")
        # for el in all_form_kwargs:
        #    dg = form_data.get(el, "")
        #    if dg == "":
        #        self.cou += 1
        #    dic.update({f"{el}": dg})
        await self.memory_state.set_state(UserStates.empty)

        return {
            "text": await self.text.get_text(
                key="change_form",
                **form_data,
            ),
            "reply_markup": await self.reply_marcup.get_marcup("change_form"),
        }

    async def change_form_state(self):
        data = await self.memory_state.get_data()
        change_form_state = data.get("change_form_state")
        # if data.get("form_data") is None:
        #    await self.memory_state.update_data({"form_data": {}})

        form_data: dict = data.get("form_data")
        if form_data is None:
            form_data = {}
            await self.memory_state.update_data({"form_data": {}})
        # ic(form_data)
        # ic(data)

        if change_form_state == "desired_date" and not await self._is_date(
            self.msg.text
        ):
            await self.msg.answer(
                self.text._stock["change_form_state"].get("desired_date")
            )
        else:
            # ic(self.msg.text)
            # ic(change_form_state)
            form_data.update({change_form_state: self.msg.text})
            await self.memory_state.update_data({"form_data": form_data})
            # await asyncio.sleep(0.1)

            if len(form_data) == len(self.text._stock.get("change_form_state")):
                text_dict: dict = await self._send_change_form_message()
            else:
                list_states = list(self.text._stock["change_form_state"])
                state_index = list_states.index(change_form_state)
                # await self.memory_state.set_state(list_states[state_index + 1])
                await self.memory_state.update_data(
                    {"change_form_state": list_states[state_index + 1]}
                )
                # ic(list_states[state_index + 1])
                text_dict = {
                    "text": self.text._stock["change_form_state"].get(
                        list_states[state_index + 1]
                    )
                }
            await self.msg.answer(**text_dict)
            # await self.msg.answer(**await self._send_change_form_message())

    async def leave_review(self):
        await self.call.message.answer(await self.text.get_text("send_me_comment"))
        await self.states.send_me_comment_message.set()

    async def send_me_comment_message(self):
        text = await self.text.get_text(
            "new_comment", username=self.msg.from_user.username, text=self.msg.text
        )
        await bot.send_message(CHANNEL_ID, text)
        # await asyncio.sleep(0.1)
        for u in ADMINS_LIST:
            try:
                await bot.send_message(u, text)
            except:  # noqa: E722
                pass
        await self.msg.answer(await self.text.get_text("message_sent"))
        await self.empty()
        await self.memory_state.finish()

    async def should_we_send_form(self):
        self.key_data = "should_we_send_form"
        form_data: dict = await self.memory_state.get_data()
        form_data: dict = form_data.get("form_data")
        if len(form_data) < len(self.text._stock.get("change_form_state")):
            await self.call.answer(
                await self.text.get_text("you_must_fill_blanks"), show_alert=True
            )
            return

        text = await self.text.get_text(
            "new_booking",
            username=self.call.from_user.username,
            text=await self.text.get_text(
                key="change_form",
                **form_data,
            ),
        )
        for a in ADMINS_LIST:
            try:
                await bot.send_message(
                    chat_id=a,
                    text=text,
                ),
            except:  # noqa: E722
                pass

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
        ),
        await self.call.message.delete()
        await gs.write_book_data(form_data)
        await self.call.message.answer(await self.text.get_text("form_sent"))
        await self.empty()
        await self.memory_state.finish()

    async def contact_manager(self):
        await self.call.message.answer(
            await self.text.get_text("manager_contact", username=MANAGER_USERNAME)
        )

    async def view_latest_studio_news(self):
        await self.call.message.delete()
        await self.call.message.answer(await self.text.get_text("last_studio_new"))

        mailings = self.db.get_all_mailings()

        is_empty = True
        for i in range(1, len(mailings) + 1):
            try:
                await bot.copy_message(
                    chat_id=self.call.from_user.id,
                    from_chat_id=mailings[-i][1],
                    message_id=mailings[-i][0],
                )
                is_empty = False
                break
            except:  # noqa: E722
                pass
        if is_empty is True:
            await self.call.message.answer(await self.text.get_text("no_mailing"))

        await asyncio.sleep(0.1)

        await self.empty()

    async def admin_menu(self):
        if self.msg.from_user.id in ADMINS_LIST:
            await self.msg.answer(
                await self.text.get_text("admin_menu"),
                reply_markup=await self.reply_marcup.get_marcup("admin_menu"),
            )
        else:
            await self.empty()

    async def mail_to_all_users(self):
        await self.memory_state.set_state(self.states.admin_send_post)
        await self.call.message.answer(await self.text.get_text("admin_send_post"))

    async def admin_send_post(self):
        await self.memory_state.finish()
        users_id = self.db.get_all_users()
        cou = 0
        # ic(users_id)
        for u in users_id:
            try:
                await bot.copy_message(
                    u[0], from_chat_id=self.msg.chat.id, message_id=self.msg.message_id
                )
            except Exception as ex:  # noqa: E722
               pass
            cou += 1
        await self.msg.answer(await self.text.get_text("admin_post_sent", cou=cou))
        self.db.insert_post(self.msg.chat.id, self.msg.message_id)
