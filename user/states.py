from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from create_bot import loop
import asyncio
from icecream import ic


class UserStates(StatesGroup):
    enter_date = State()

    change_form_state = State()

    def __init__(self, state_name: str):
        self.state: FSMContext = getattr(UserStates, str(state_name), None)

        self.state_name = state_name
        # self.stock = {
        #    UserStates.get_recipe: "",
        # }
