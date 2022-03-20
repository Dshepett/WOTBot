from aiogram.dispatcher.filters.state import StatesGroup, State


class ChooseCharacteristics(StatesGroup):
    Base = State()
    ChoseHealth = State()
    ChoseDamage = State()
    ChoseArmor = State()
    ChoseSpeed = State()    
