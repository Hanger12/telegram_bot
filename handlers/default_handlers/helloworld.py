from telebot.types import Message
from loader import bot


@bot.message_handler(commands=["helloworld"])
def bot_helloworld(message: Message):
    bot_info = bot.get_me()
    bot.reply_to(message, f"Название бота: {bot_info.full_name}\n"
                          f"ID бота: {bot_info.id}\n"
                          f"Приветствие: Вас приветствует телеграмм-бот myGameStore."
                          f"Здесь вы можете посмотреть интересующие вас игры, рейтинг, год выпуска на различные "
                          f"платформы,"
                          f"а также актуальные цены.")
