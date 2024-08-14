from telebot.handler_backends import State, StatesGroup


class StateCustom(StatesGroup):
    search_count = State()
    next_page = State()
