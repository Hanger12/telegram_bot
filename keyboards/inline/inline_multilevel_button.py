from typing import Optional
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

platform_dict = {"Playstation 5": 187,
                 "Xbox Series S/X": 186,
                 "Playstation 4": 18,
                 "Xbox One": 1,
                 "Nintendo Switch": 7,
                 "Pc": 4}


def inline_yes_no_button(number: int = 1) -> InlineKeyboardMarkup:
    """Много-уровневая инлайн клавиатруа кнопки, да и нет"""
    yes_no_keyboard = InlineKeyboardMarkup(row_width=2)
    button1 = InlineKeyboardButton(text="Да", callback_data=f"Yes {number}")
    button2 = InlineKeyboardButton(text="Нет", callback_data=f"No {number}")
    button3 = InlineKeyboardButton(text="Назад в главное меню", callback_data="back_mainmenu")
    yes_no_keyboard.add(button1, button2)
    yes_no_keyboard.add(button3)
    return yes_no_keyboard


def inline_search_button() -> InlineKeyboardMarkup:
    """Много-уровневая инлайн клавиатруа кнопки, найти и назад"""
    keyboard = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton(text="Найти", callback_data="Search")
    button2 = InlineKeyboardButton(text="Назад в главное меню", callback_data="back_mainmenu")
    keyboard.add(button1)
    keyboard.add(button2)
    return keyboard


def inline_platform_button(platform_id_list=None) -> InlineKeyboardMarkup:
    """Много-уровневая инлайн клавиатруа, выбор платформы"""
    if platform_id_list is None:
        platform_id_list = []
    platforms = InlineKeyboardMarkup()
    for platform, id_platform in platform_dict.items():
        if id_platform in platform_id_list:
            continue
        platforms.add(InlineKeyboardButton(text=platform, callback_data=f"platform: {id_platform}"))
    platforms.add(InlineKeyboardButton(text="Далее", callback_data="Continue"),
                  InlineKeyboardButton(text="Назад", callback_data="Back 1"))
    platforms.add(InlineKeyboardButton(text="Назад в главное меню", callback_data="back_mainmenu"))
    return platforms
