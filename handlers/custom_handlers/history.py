from loader import bot
from telebot.types import Message

from states.history_state import StateHistory
from utils.misc.displaying_games import display_game, back_main_menu
from utils.misc.inserts_data import get_user
from keyboards.inline.inline_history_command import inline_command, inline_command_data, inline_back_main_menu, \
    inline_back_history
from api.rawg_api_search import get_game
import json


@bot.message_handler(commands=["history"])
def history_command(message: Message) -> None:
    """Обработчик Команды history"""
    user_id = message.from_user.id
    user = get_user(user_id)
    if user is None:
        bot.send_message(message.chat.id, "Для начала вам нужно зарегистрироваться. "
                                          "Введите команду /start или напишите мне привет")
        return
    if inline_command(user) is None:
        bot.send_message(chat_id=message.chat.id, text="у вас нет использованных команд",
                         reply_markup=inline_back_main_menu())
    else:
        bot.send_message(chat_id=message.chat.id, text="Вы пользовались командами:", reply_markup=inline_command(user))
    bot.set_state(user_id, StateHistory.next_page, message.chat.id)


@bot.callback_query_handler(state=StateHistory.next_page, func=lambda call: True)
def callback(call):
    call_data = call.data.split("-")
    if call_data[0] == "commands:":
        if inline_command_data(int(call_data[1])) is None:
            bot.send_message(chat_id=call.message.chat.id, text="В этой команде нету данных",
                             reply_markup=inline_back_history())
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f"Команда: {call_data[2]}",
                              reply_markup=inline_command_data(int(call_data[1])))
    elif call_data[0] == "command_data:":
        if call_data[1] == "/low":
            with bot.retrieve_data(user_id=call.from_user.id) as data_dict:
                data_dict["low_command"] = {
                    "data": {
                        "platforms": json.loads(call_data[2]),
                        "page_size": int(call_data[3]),
                        "platforms_count": 1,
                        "page": 1
                    }
                }
            game_result = get_game(data_dict["low_command"]["data"])
            display_game(message=call.message, data=game_result, page=data_dict["low_command"]["data"]["page"])
        elif call_data[1] == "/custom":
            with bot.retrieve_data(user_id=call.from_user.id) as data_dict:
                data_dict["custom_command"] = {
                    "data": {
                        "page_size": int(call_data[3]),
                        "page": 1
                    }
                    }
                if call_data[2] != "[]":
                    data_dict["custom_command"]["data"]["platforms"] = json.loads(call_data[2])
                if call_data[4] != 'None':
                    data_dict["custom_command"]["data"]["developers"] = int(call_data[4])
                if call_data[5] != 'None':
                    data_dict["custom_command"]["data"]["genres"] = call_data[5]
            games_result = get_game(data=data_dict["custom_command"]["data"])
            display_game(message=call.message, data=games_result, page=data_dict["custom_command"]["data"]['page'])
        elif call_data[1] == "/high":
            with bot.retrieve_data(user_id=call.from_user.id) as data_dict:
                data_dict["high_command"] = {
                    "data": {
                        "platforms": json.loads(call_data[2]),
                        "page_size": int(call_data[3]),
                        "genres": call_data[5],
                        "page": 1
                    }
                }
                data_dict["high_command"]["data"]["platforms_count"] = len(
                    data_dict["high_command"]["data"]["platforms"])
            games_result = get_game(data_dict["high_command"]["data"])
            display_game(message=call.message, data=games_result, page=data_dict["high_command"]["data"]['page'])
    elif call.data == "back_mainmenu":
        back_main_menu(chat_id=call.message.chat.id, user=call.from_user)
    elif call.data == "Back":
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Вы пользовались командами:",
                              reply_markup=inline_command(get_user(call.from_user.id)))


@bot.message_handler(state=StateHistory.next_page)
def next_page(message: Message) -> None:
    """Обработчик страниц, отображаемых игр"""
    if message.text.upper() == "В НАЧАЛО":
        back_main_menu(chat_id=message.chat.id, user=message.from_user)
    elif message.text.title() == "Дальше":
        with bot.retrieve_data(user_id=message.from_user.id) as data_dict:
            if "high_command" in data_dict:
                data_dict["high_command"]["data"]['page'] += 1
                games_result = get_game(data_dict["high_command"]["data"])
                display_game(message=message, data=games_result, page=data_dict["high_command"]["data"]['page'])
            elif "low_command" in data_dict:
                data_dict["low_command"]["data"]['page'] += 1
                games_result = get_game(data_dict["low_command"]["data"])
                display_game(message=message, data=games_result, page=data_dict["low_command"]["data"]['page'])
            elif "custom_command" in data_dict:
                data_dict["custom_command"]["data"]['page'] += 1
                games_result = get_game(data_dict["custom_command"]["data"])
                display_game(message=message, data=games_result, page=data_dict["custom_command"]["data"]['page'])
