from telebot.handler_backends import State, StatesGroup


class StateHigh(StatesGroup):
    search_count = State()
    next_page = State()

