import user.handlers  # noqa: F401
from major.middlewear import UsersLastActionMiddlewear
from major.reminder import reminder_func

# import asyncio

# import admin
from create_bot import dp, loop

from aiogram.utils import executor


# loop = asyncio.get_event_loop()
# loop.create_task(check_admin_offer())
if __name__ == "__main__":
    dp.middleware.setup(UsersLastActionMiddlewear())
    loop.create_task(reminder_func())

    executor.start_polling(dp, skip_updates=True)
