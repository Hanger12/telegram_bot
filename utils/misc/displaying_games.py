from api.rawg_api_search import get_stores_buy
from keyboards.inline.inline_store import get_button_stores
from telebot.types import InputMediaPhoto, Message
from telebot.apihelper import ApiTelegramException
from keyboards.reply.button_platform import display_page_reply, reply_back
from database.models import User
from keyboards.reply.button_platform import hide_keyboad_markup
from loader import bot


def display_game(message: Message, data: dict, page: int):
    if 'results' not in data:
        bot.send_message(message.chat.id, text="Это последняя страница возвращаюсь в начало!")
        back_main_menu(chat_id=message.chat.id, user=message.from_user)
        return
    if page >= 6:
        bot.send_message(message.chat.id, text="Превышен лимит страниц возвращаюсь в начало!")
        back_main_menu(chat_id=message.chat.id, user=message.from_user)
        return
    for game in data['results']:
        bot.send_message(message.chat.id, "Название игры: " + game['name'])
        bot.send_message(message.chat.id, "Платформа: " + ', '.join([platform['platform']['name']
                                                                     for platform in game["platforms"]]))
        try:
            bot.send_media_group(message.chat.id, media=[InputMediaPhoto(media=screenshots['image'])
                                                         for screenshots in game['short_screenshots']])
        except (ApiTelegramException, TypeError):
            bot.send_message(message.chat.id, "Скриншоты данной игры загрузить не удалось")
        bot.send_message(message.chat.id, "Жанр: " + ' '.join([genre['name']
                                                               for genre in game["genres"]]))
        keyboard = get_button_stores(game['stores'], get_stores_buy(game['id']))
        if keyboard is None:
            bot.send_message(message.chat.id, "Игра еще не вышла, покупка не доступна")
        else:
            bot.send_message(message.chat.id, text='Где купить?',
                             reply_markup=keyboard)
    else:
        if data["results"]:
            bot.send_message(message.chat.id, "Вывести еще игры? нажмите на кнопку ниже",
                             reply_markup=display_page_reply())
        else:
            bot.send_message(message.chat.id, "Ничего не нашел. \U0001F97A Попробуйте ввести другие параметры",
                             reply_markup=reply_back())


def back_main_menu(chat_id, user) -> None:
    bot.set_state(user.id, state=None, chat_id=chat_id)
    bot.send_message(chat_id, "Вы вернулись в главное меню", reply_markup=hide_keyboad_markup())
    user_name = User.get_or_none(User.user_id == user.id)
    bot.send_message(chat_id,
                     f"Рад снова вас приветствовать, {user_name.first_name},в магазине игр.\n"
                     f"Для навигации воспользуйтесь блоком меню.", reply_markup=None)
