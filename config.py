import datetime
import os
import sys

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from loguru import logger
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from peewee import SqliteDatabase

from db.settings import *


# Загружаем переменные из файла .env

load_dotenv()

# service settings
SECRET_KEY = os.getenv('SECRET_KEY')
ACCOUNT_NAME = os.getenv('ACCOUNT_NAME')

# configure bot.
tgToken = os.getenv("TELEBOT_TOKEN")
bot = Bot(token=tgToken)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# telegram API settings
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
with open("./db/session.txt", 'r', encoding='utf-8') as f:
    SESSION_STRING = f.read()

# set admins list
me = os.getenv("ME_TELEGRAM_ID")
admins_list = [me]
DEBUG = int(os.getenv("DEBUG"))
if not DEBUG:
    admins_list.extend({})


class EMOJI:
    sad = '😞'
    like = '👍'
    hello = '👋'


#  ********** LOGGER CONFIG ********************************
LOGGING_DIRECTORY = 'logs'
LOGGING_FILENAME = 'discord_mailer.log'
PATH = os.getcwd()
if not os.path.exists('./logs'):
    os.mkdir("./logs")
today = datetime.datetime.today().strftime("%Y-%m-%d")
file_path = os.path.join(PATH, LOGGING_DIRECTORY, today, LOGGING_FILENAME)
LOG_LEVEL = "WARNING"
DEBUG_LEVEL = "INFO"
if DEBUG:
    DEBUG_LEVEL = "DEBUG"
logger_cfg = {
    "handlers": [
        {
            "sink": sys.stdout,
            "level": DEBUG_LEVEL,
            "format": "<white>{time:HH:mm:ss}</white> - <yellow>{level}</yellow> | <green>{message}</green>"
        },
        {
            "sink": file_path, "level": LOG_LEVEL,
            "format": "{time:YYYY-MM-DD HH:mm:ss} - {level} | {message}",
            "rotation": "50 MB"
        },
    ]
}
logger.configure(**logger_cfg)
logger.info('Start logging to:', file_path)
#  ********** END OF LOGGER CONFIG *************************


#  ********** DATABASE CONFIG *************************

db_file_name = 'db/users.db'
full_path = os.path.join(PATH, db_file_name)
db = SqliteDatabase(
    full_path,
    pragmas={
        'journal_mode': 'wal',
        'cache_size': -1 * 64000,
        'foreign_keys': 1,
        'ignore_check_constraints': 0,
        'synchronous': 0
    }
)

#  ********** END OF DATABASE CONFIG *************************


#  *************** GETCOUSE API CONFIG ****************************

REQUEST_LIMIT = 5
KICK_RATE = kick_rate
REQUEST_RATE = admin_rate

#  ********** END OF GETCOUSE API  CONFIG *************************
