from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    enter_date = State()

    def __init__(self):
        self.stock = {
            str(UserStates.enter_date): "",
        }
        # self.now_state = state
