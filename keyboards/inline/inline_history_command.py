from typing import List, Optional

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models import CommandData
import re


def inline_command(user) -> Optional[InlineKeyboardMarkup]:
    command_markup = InlineKeyboardMarkup(row_width=1)
    commands: List = user.command
    if len(commands) == 0:
        return None
    command_button = [InlineKeyboardButton(text=command.title, callback_data=f"commands:-{command.command_id}-"
                                                                             f"{command.title}")
                      for command in commands]
    command_markup.add(*command_button)
    command_markup.add(InlineKeyboardButton(text="Назад в главное меню", callback_data="back_mainmenu"))
    return command_markup


def inline_command_data(command_id) -> Optional[InlineKeyboardMarkup]:
    commands_data_markup = InlineKeyboardMarkup(row_width=1)
    commands_data = (CommandData.select().where(CommandData.command == command_id)
                     .order_by(-CommandData.command_data_id)
                     .limit(10))
    if commands_data is None:
        return None
    command_data_button = [InlineKeyboardButton(text=str(command_data),
                                                callback_data=f"command_data:-"
                                                              f"{command_data.command.title}-"
                                                              f"{command_data.platforms}-"
                                                              f"{command_data.page_size}-"
                                                              f"{command_data.developers}-"
                                                              f"{command_data.genres}") for
                           command_data in commands_data]
    commands_data_markup.add(*command_data_button)
    commands_data_markup.add(InlineKeyboardButton(text="Назад", callback_data="Back"))
    commands_data_markup.add(InlineKeyboardButton(text="Назад в главное меню", callback_data="back_mainmenu"))
    return commands_data_markup


def inline_back_history() -> InlineKeyboardMarkup:
    back_keyboard = InlineKeyboardMarkup(row_width=1)
    back_keyboard.add(InlineKeyboardButton(text="Назад", callback_data="Back"))
    back_keyboard.add(InlineKeyboardButton(text="Назад в главное меню", callback_data="back_mainmenu"))
    return back_keyboard


def inline_back_main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup().add(InlineKeyboardButton(text="Назад в главное меню", callback_data="back_mainmenu"))
