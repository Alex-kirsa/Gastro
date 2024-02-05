from aiogram.dispatcher.middlewares import BaseMiddleware
from database import Database
from aiogram import types


class UsersLastActionMiddlewear(BaseMiddleware):
    def __init__(self):
        super().__init__()
        # self.data = data_obj

    async def on_pre_process_message(self, message: types.Message, data: dict):
        db = Database()
        db.check_user_in_db(message.from_user.id, message.from_user.username)
        db.update_datetime(message.from_user.id)
        del db
