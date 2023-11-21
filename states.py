from aiogram.dispatcher.filters.state import StatesGroup, State


class ProfileStatesGroup(StatesGroup):
    horizon = State()
    clarify = State()
    pk = State()
    other = State()
    ustraneno = State()
    reset = State()
    choose_problem_cat = State()
    it_problem_login = State()
    it_problem_awp = State()
    it_problem_workplace = State()
    it_problem_info = State()
    oborudovaniye_workplace = State()
    oborudovaniye_info = State()
    it_problem_photo = State()
    it_problem_video = State()
    it_problem_nothing = State()
    oborudovaniye_number = State()
    oborudovaniye_desc = State()

class AdminStatesGroup(StatesGroup):
    chat_id = State()
    message = State()
