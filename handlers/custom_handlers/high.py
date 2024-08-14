from keyboards.inline.inline_multilevel_button import inline_platform_button
from loader import bot
from telebot.types import Message
from states.high_state import StateHigh
from keyboards.inline.inline_genres import get_button_genres
from api.rawg_api_search import get_game
from utils.misc.displaying_games import display_game, back_main_menu
from utils.misc.inserts_data import get_user, insert_command, insert_command_data


@bot.message_handler(commands=['high'])
def command_high(message: Message) -> None:
    """Начальный обработчик команды /high"""
    user_id = message.from_user.id
    if get_user(user_id) is None:
        bot.send_message(message.chat.id, "Для начала вам нужно зарегистрироваться. "
                                          "Введите команду /start или напишите мне привет")
        return
    bot.set_state(user_id, StateHigh.search_count, message.chat.id)
    bot.send_message(user_id,
                     "Выберите предпочтительные платформы,\n"
                     "для которых может быть доступна игра и нажмите далее (Можно выбрать несколько):",
                     reply_markup=inline_platform_button())
    with bot.retrieve_data(user_id=user_id, chat_id=message.chat.id) as data_high:
        data_high["high_command"] = {"user_id": user_id,
                                     "title": "/high"}
    insert_command(user_id=user_id, command_name="high_command", data=data_high)
    with bot.retrieve_data(user_id=user_id, chat_id=message.chat.id) as data_high:
        data_high["high_command"]["data"] = {"platforms": [], "page": 1}


@bot.callback_query_handler(state=StateHigh.search_count, func=lambda call: True)
def genre(call) -> None:
    """Метод Callback для инлайн клавиатуры"""
    with bot.retrieve_data(user_id=call.from_user.id) as data_high:
        if call.data.split()[0] == "genres:":
            data_high["high_command"]["data"]["genres"] = call.data.split()[1]
            bot.send_message(call.message.chat.id, "Сколько игр отобразить (от 1 до 10)?")
        elif call.data.split()[0] == "platform:":
            data_high["high_command"]["data"]["platforms"].append(int(call.data.split()[1]))
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Можете выбрать ещё одну платформу:",
                                  reply_markup=inline_platform_button(data_high["high_command"]["data"]["platforms"]))
        elif call.data == "Continue":
            if data_high["high_command"]["data"]["platforms"]:
                bot.edit_message_text(chat_id=call.message.chat.id,
                                      message_id=call.message.message_id,
                                      text="Выбери жанр игры:",
                                      reply_markup=get_button_genres())
            else:
                bot.send_message(chat_id=call.message.chat.id,
                                 text="Нужно выбрать хотя бы одну платформу")
    if call.data == "Back":
        data_high["high_command"]["data"]["platforms"].clear()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Выберите предпочтительные платформы,\n"
                                   "для которых может быть доступна игра и нажмите далее "
                                   "(Можно выбрать несколько):",
                              reply_markup=inline_platform_button())
    elif call.data == "back_mainmenu":
        back_main_menu(chat_id=call.message.chat.id, user=call.from_user)
    print(data_high)


def display_game_multiplatform(message: Message, data: dict):
    """Метод для отображения игр ботом"""
    games_result = get_game(data["high_command"]["data"])
    display_game(message=message, data=games_result, page=data["high_command"]["data"]['page'])


@bot.message_handler(state=StateHigh.search_count)
def get_search_count(message: Message):
    """Конечный обработчик, ждущий ответ от пользователя"""
    if message.text.upper() == "В НАЧАЛО":
        back_main_menu(chat_id=message.chat.id, user=message.from_user)
    elif message.text.isdigit() and 0 < int(message.text) < 11:
        bot.send_message(message.chat.id, "Отлично держите ваши игры")
        with bot.retrieve_data(user_id=message.from_user.id) as data_high:
            data_high["high_command"]["data"]['page_size'] = int(message.text)
            data_high["high_command"]["data"]["platforms_count"] = len(data_high["high_command"]["data"]["platforms"])
        display_game_multiplatform(message, data_high)
        insert_command_data(user_id=message.from_user.id, command_name="high_command", data=data_high)
        bot.set_state(message.from_user.id, state=StateHigh.next_page, chat_id=message.chat.id)
    else:
        bot.send_message(message.chat.id, "вы ввели не число или превысили лимит ввода! попробуйте еще раз")


@bot.message_handler(state=StateHigh.next_page)
def next_page(message: Message) -> None:
    """Обработчик страниц, отображаемых игр"""
    if message.text.upper() == "В НАЧАЛО":
        back_main_menu(chat_id=message.chat.id, user=message.from_user)
    elif message.text.title() == "Дальше":
        with bot.retrieve_data(message.from_user.id) as data_high:
            data_high["high_command"]["data"]["page"] += 1
        display_game_multiplatform(message, data_high)
