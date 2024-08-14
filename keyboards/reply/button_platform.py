from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

platform_dict = {"Playstation 5": 187,
                 "Xbox Series S/X": 186,
                 "Playstation 4": 18,
                 "Xbox One": 1,
                 "Nintendo Switch": 7,
                 "Pc": 4}


def display_platform_reply() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for platform in platform_dict:
        keyboard.add(KeyboardButton(text=platform))
    keyboard.add(KeyboardButton(text="В начало"))
    return keyboard


def display_page_reply() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text='Дальше'))
    keyboard.add(KeyboardButton(text="В начало"))
    return keyboard


def reply_back() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text="В начало"))
    return keyboard


def hide_keyboad_markup() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
