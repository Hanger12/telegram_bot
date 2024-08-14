from typing import Optional

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.rawg_api_search import get_genres


def get_button_genres() -> Optional[InlineKeyboardMarkup]:
    """Метод создающий инлайн клавиатуру с жанрами"""
    keyboard_genres = InlineKeyboardMarkup(row_width=3)
    genres = [InlineKeyboardButton(text=genre['name'], callback_data="genres: " + genre['slug'])
              for genre in get_genres()]
    keyboard_genres.add(*genres)
    keyboard_genres.add(InlineKeyboardButton(text="Назад", callback_data="Back 2"))
    return keyboard_genres
