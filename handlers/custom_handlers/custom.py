from api.rawg_api_search import get_game
from loader import bot
from telebot.types import Message
from keyboards.inline.inline_multilevel_button import inline_yes_no_button, inline_platform_button, inline_search_button
from keyboards.inline.inline_genres import get_button_genres
from keyboards.inline.inline_developer import get_button_developers
from states.custom_state import StateCustom
from utils.misc.displaying_games import display_game, back_main_menu
from utils.misc.inserts_data import insert_command, insert_command_data, get_user

count_level = 1


@bot.message_handler(commands=['custom'])
def command_custom(message: Message) -> None:
    user_id = message.from_user.id
    if get_user(user_id) is None:
        bot.send_message(message.chat.id, "Для начала вам нужно зарегистрироваться. "
                                          "Введите команду /start или напишите мне привет")
        return
    bot.send_message(message.chat.id, "Выбрать платформу?", reply_markup=inline_yes_no_button())
    bot.set_state(message.from_user.id, StateCustom.search_count, message.chat.id)
    with bot.retrieve_data(user_id) as data_custom:
        data_custom["custom_command"] = {"user_id": user_id, "title": "/custom"}
    insert_command(user_id=user_id,command_name="custom_command", data=data_custom)
    with bot.retrieve_data(user_id=user_id, chat_id=message.chat.id) as data_custom:
        data_custom["custom_command"]["data"] = {"platforms": [], "page": 1}


@bot.callback_query_handler(state=StateCustom.search_count, func=lambda call: True)
def callback(call):
    """Обработчик инлайн клавиатуры бота в команде /custom"""
    call_data = call.data.split()
    message_text = ""
    reply = inline_yes_no_button()
    print(call_data)
    with bot.retrieve_data(user_id=call.from_user.id) as data_custom:
        if call_data[0] == "developers:":
            data_custom["custom_command"]["data"]["developers"] = int(call_data[1])
            message_text = "Нажмите кнопку найти"
            reply = inline_search_button()
        elif call.data.split()[0] == "genres:":
            data_custom["custom_command"]["data"]["genres"] = call_data[1]
            message_text = "Выбрать разработчика игры?"
            reply = inline_yes_no_button()
        elif call.data.split()[0] == "platform:":
            data_custom["custom_command"]["data"]["platforms"].append(int(call_data[1]))
            message_text = "Можете выбрать ещё одну платформу:"
            reply = inline_platform_button(data_custom["custom_command"]["data"]["platforms"])
    if call_data[0] == "Yes":
        if call_data[1] == "1":
            message_text = ("Выберите предпочтительные платформы,\nдля которых может быть доступна игра и нажмите "
                            "далее (Можно выбрать несколько):")
            reply = inline_platform_button()
        elif call_data[1] == "2":
            message_text = "Выберите жанр игры:"
            reply = get_button_genres()
        elif call_data[1] == "3":
            message_text = "Выберите разработчика игры:"
            reply = get_button_developers()
    elif call_data[0] == "No":
        if call_data[1] == "1":
            message_text = "Выбрать жанр игры?"
            reply = inline_yes_no_button(2)
        elif call_data[1] == "2":
            message_text = "Выбрать разработчика игры?"
            reply = inline_yes_no_button(3)
        elif call_data[1] == "3":
            message_text = "Нажмите кнопку найти"
            reply = inline_search_button()
    elif call.data == "Search":
        message_text = "Сколько игр отобразить (от 1 до 10)?"
        reply = None
    elif call.data == "Continue":
        if data_custom["custom_command"]["data"]["platforms"]:
            message_text = "Выбрать жанр игры?"
            reply = inline_yes_no_button(2)
        else:
            bot.send_message(chat_id=call.message.chat.id,
                             text="Нужно выбрать хотя бы одну платформу")
    elif call_data[0] == "Back":
        if call_data[1] == "1":
            data_custom["custom_command"]["data"]["platforms"].clear()
            message_text = "Выбрать платформу?"
            reply = inline_yes_no_button()
        elif call_data[1] == "2":
            message_text = "Выбрать жанр игры?"
            reply = inline_yes_no_button(2)
        elif call_data[1] == "3":
            message_text = "Выбрать разработчика игры?"
            reply = inline_yes_no_button(3)
    elif call.data == "back_mainmenu":
        back_main_menu(chat_id=call.message.chat.id, user=call.from_user)
    if message_text:
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=message_text,
                              reply_markup=reply if reply is not None else None)


@bot.message_handler(state=StateCustom.search_count)
def get_search_count(message: Message) -> None:
    """Метод для отображения игр ботом"""
    if message.text.isdigit() and 0 < int(message.text) < 11:
        bot.send_message(message.chat.id, "Отлично держите ваши игры")
        with bot.retrieve_data(user_id=message.from_user.id) as data_custom:
            data_custom["custom_command"]["data"]['page_size'] = int(message.text)
            if data_custom["custom_command"]["data"]["platforms"]:
                data_custom["custom_command"]["data"]["platforms_count"] = len(
                    data_custom["custom_command"]["data"]["platforms"])
        display_game_custom_search(message, data_custom)
        insert_command_data(user_id=message.from_user.id,command_name="custom_command", data=data_custom)
        bot.set_state(message.from_user.id, state=StateCustom.next_page, chat_id=message.chat.id)
    else:
        bot.send_message(message.chat.id, "вы ввели не число или превысили лимит ввода! попробуйте еще раз")


@bot.message_handler(state=StateCustom.next_page)
def next_page(message: Message) -> None:
    if message.text.upper() == "В НАЧАЛО":
        back_main_menu(chat_id=message.chat.id, user=message.from_user)
    elif message.text.title() == "Дальше":
        with bot.retrieve_data(user_id=message.from_user.id) as data_custom:
            data_custom["custom_command"]["data"]['page'] += 1
        display_game_custom_search(message, data_custom)


def display_game_custom_search(message: Message, data: dict):
    games_result = get_game(data["custom_command"]["data"])
    display_game(message=message, data=games_result, page=data["custom_command"]["data"]['page'])
