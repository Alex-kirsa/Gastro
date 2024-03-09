import asyncio
from database import Database
from create_bot import bot
from user.text import UserText
from icecream import ic
from config import REMINDER_SECS
from aiogram.utils.exceptions import ChatNotFound


async def reminder_func():
    while True:
        ic("reminder")
        db = Database()
        user_text = UserText()
        users_have_to_reminder = db.get_users_out_of_datetime()
        for user_id in users_have_to_reminder:
            user_id = user_id[0]
            try:
                await bot.send_message(user_id, await user_text.get_text("reminder"))
                db.update_datetime(user_id)
            except:  # noqa: E722
                pass
                # await db.delete_user(user_id)

        del db, user_text, users_have_to_reminder
        await asyncio.sleep(REMINDER_SECS)
        # await asyncio.sleep(60 * 60 * 24)
