import asyncio

from aiogram.utils import executor
# from config.check_new_member import *
import user
# import admin
from create_bot import dp


#loop = asyncio.get_event_loop()
#loop.create_task(check_admin_offer())
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

