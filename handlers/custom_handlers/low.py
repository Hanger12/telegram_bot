from loader import bot
from telebot.types import Message
from states.low_state import StateLow
from keyboards.reply.button_platform import display_platform_reply, platform_dict, hide_keyboad_markup
from api.rawg_api_search import get_game
from utils.misc.displaying_games import display_game, back_main_menu
from utils.misc.inserts_data import get_user, insert_command, insert_command_data


@bot.message_handler(commands=['low'])
def command_low(message: Message) -> None:
    """Обработчик команды /low"""
    user_id = message.from_user.id
    if get_user(user_id) is None:
        bot.send_message(message.chat.id, "Для начала вам нужно зарегистрироваться. "
                                          "Введите команду /start или напишите мне привет")
        return
    bot.set_state(user_id, StateLow.platform_name, message.chat.id)
    bot.send_message(message.chat.id, "Хорошо, выбери платформу для которой найти эксклюзивные игры:",
                     reply_markup=display_platform_reply())
    with bot.retrieve_data(user_id) as data_low:
        data_low["low_command"] = {"user_id": user_id,
                                   "title": "/low"}
    insert_command(user_id=user_id, command_name="low_command", data=data_low)
    with bot.retrieve_data(user_id) as data_low:
        data_low["low_command"]["data"] = {"page": 1}


@bot.message_handler(state=StateLow.platform_name)
def get_platform(message: Message) -> None:
    """Состояние, при котором пользователь должен выбрать платформу"""
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data_low:
        if message.text.upper() == "В НАЧАЛО":
            back_main_menu(chat_id=message.chat.id, user=message.from_user)
        elif message.text.title() not in platform_dict:
            bot.send_message(message.from_user.id, "Упс, не нашел такой платформы!")
        else:
            data_low["low_command"]["data"]['platforms'] = platform_dict[message.text.title()]
            bot.set_state(message.from_user.id, StateLow.search_count, message.chat.id)
            bot.send_message(message.from_user.id,
                             "Теперь введите количество игр, которое нужно отобразить (минимально 1,"
                             "максимально 10):", reply_markup=hide_keyboad_markup())


@bot.message_handler(state=StateLow.search_count)
def get_search_count(message: Message) -> None:
    """Состояние, при котором пользователь должен ввести количество игр, которое нужно отобразить"""
    if message.text.upper() == "В НАЧАЛО":
        back_main_menu(chat_id=message.chat.id, user=message.from_user)
    elif message.text.isdigit() and 0 < int(message.text) < 11:
        bot.send_message(message.chat.id, "Отлично держите ваши эксклюзивы")
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_low:
            data_low["low_command"]["data"]['page_size'] = int(message.text)
            data_low["low_command"]["data"]["platforms_count"] = 1
        insert_command_data(user_id=message.from_user.id, command_name="low_command", data=data_low)
        display_game_exclusive(message, data_low)
        bot.set_state(message.from_user.id, state=StateLow.next_page, chat_id=message.chat.id)
    else:
        bot.send_message(message.chat.id, "вы ввели не число или превысили лимит ввода! попробуйте еще раз")


@bot.message_handler(state=StateLow.next_page)
def next_page(message: Message) -> None:
    """Обработчик страниц, отображаемых игр"""
    if message.text.upper() == "В НАЧАЛО":
        back_main_menu(chat_id=message.chat.id, user=message.from_user)
    elif message.text.title() == "Дальше":
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data_low:
            data_low["low_command"]["data"]['page'] += 1
        display_game_exclusive(message, data_low)


def display_game_exclusive(message: Message, data: dict):
    """Метод для отображения игр ботом"""
    game_result = get_game(data=data["low_command"]["data"])
    display_game(message=message, data=game_result, page=data["low_command"]["data"]['page'])
