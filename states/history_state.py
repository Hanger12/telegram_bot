from telebot.handler_backends import State, StatesGroup


class StateHistory(StatesGroup):
    next_page = State()
