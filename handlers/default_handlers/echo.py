from telebot.types import Message

from loader import bot
from database.models import User
from handlers.default_handlers.start import bot_start


@bot.message_handler(state=None, content_types=["text"])
def bot_echo(message: Message):
    if message.text.lower() == "привет":
        bot_start(message)
