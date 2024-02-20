from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    regFirstName = State()
    regLastName = State()
