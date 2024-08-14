from telebot.types import Message
from loader import bot
from database.models import User, create_models
from peewee import IntegrityError


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    try:
        User.create(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        bot.send_message(message.chat.id,
                         f"Приветствую пользователь, {first_name},в магазине игр.\n"
                         f"Для навигации воспользуйтесь блоком меню.", reply_markup=None)
    except IntegrityError as exc:
        bot.send_message(message.chat.id,
                         f"Рад снова вас приветствовать, {first_name},в магазине игр.\n"
                         f"Для навигации воспользуйтесь блоком меню.", reply_markup=None)
