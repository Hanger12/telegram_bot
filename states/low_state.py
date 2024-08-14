from telebot.handler_backends import State, StatesGroup


class StateLow(StatesGroup):
    platform_name = State()
    search_count = State()
    next_page = State()
