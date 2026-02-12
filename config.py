import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# Пути к файлам
TAROT_IMAGES_PATH = 'images/tarot'
DATA_PATH = 'data'

# Настройки
DEFAULT_LANGUAGE = 'ru'
MAX_DAILY_READINGS = 5  # Ограничение гаданий в день на пользователя
