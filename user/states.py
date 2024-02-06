from aiogram.dispatcher.filters.state import State, StatesGroup

# from aiogram.dispatcher import FSMContext

# from create_bot import loop
# import asyncio
# from icecream import ic


class UserStates(StatesGroup):
    enter_date = State()

    change_form_state = State()

    send_me_comment_message = State()

    admin_send_post = State()

    empty = State()

    def __init__(self, state_name: str):
        self.state_name = state_name
        # self.stock = {
        #    UserStates.get_recipe: "",
        # }
