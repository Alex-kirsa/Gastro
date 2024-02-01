import asyncio
import user.handlers

# import admin
from create_bot import dp

from aiogram.utils import executor

import logging

logging.basicConfig(level=logging.INFO)

# loop = asyncio.get_event_loop()
# loop.create_task(check_admin_offer())
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False)
