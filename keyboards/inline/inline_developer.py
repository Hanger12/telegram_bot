from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

developers_dict = {
    "Ubisoft": 405,
    "Square Enix": 4132,
    "Capcom": 3678,
    "Mundfish": 24949,
    "Bethesda Softworks": 4,
    "id Software": 343}


def get_button_developers() -> InlineKeyboardMarkup:
    """Метод, создающий инлайн клавиатуру с разработчиками игр"""
    keyboard_developers = InlineKeyboardMarkup()
    for developers, id_developers in developers_dict.items():
        keyboard_developers.add(InlineKeyboardButton(text=developers, callback_data=f"developers: {id_developers}"))
    keyboard_developers.add(InlineKeyboardButton(text="Назад", callback_data="Back 3"))
    return keyboard_developers
