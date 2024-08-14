import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

DB_PATH = "database/history.db"
BOT_TOKEN = os.getenv("BOT_TOKEN")
RAWG_API_KEY = os.getenv("RAWG_API")
API_BASE_URL = "https://api.rawg.io/api/"
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("helloworld", "Описание приветствия бота"),
    ("low", "Вывести список игр, выпущенных для одной платформы (эксклюзивов)"),
    ("high", "Вывести список игр, выпущенных для нескольких платформ (мультиплатформенные игры)"),
    ("custom", "Поиск игр пользовательского диапазона"),
    ("history", "Вывести историю запросов пользователя (последние 10 запросов)")
)
