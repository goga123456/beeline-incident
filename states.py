from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileStatesGroup(StatesGroup):
    it_problem_info = State()
    it_problem_photo = State()
    it_problem_video = State()
    it_problem_nothing = State()
    oborudovaniye_number = State()
    oborudovaniye_problem_info = State()
