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
deskent = os.getenv("DESKENT_TELEGRAM_ID")
vova = os.getenv("VOVA_TELEGRAM_ID")
admins_list = [vova, deskent]
DEBUG = int(os.getenv("DEBUG"))
if not DEBUG:
    admins_list.extend(admins)


class EMOJI:
    sad = '😞'
    like = '👍'
    hello = '👋'


#  ********** LOGGER CONFIG ********************************

PATH = os.getcwd()
today = datetime.datetime.today().strftime("%Y-%m-%d")
file_path = os.path.join(os.path.relpath(PATH, start=None), 'logs', today, 'channel_admin.log')

LOG_LEVEL = "ERROR"
logger_cfg = {
   "handlers": [
       {
           "sink": sys.stdout,
           "level": "INFO",
           "format": "<white>{time:HH:mm:ss}</white> - <yellow>{level}</yellow> | <green>{message}</green>"
       },
       {
            "sink": file_path, "level": LOG_LEVEL,
            "format": "{time:YYYY-MM-DD HH:mm:ss} - {level}: || {message} ||",
            "rotation": "50 MB"
       },
    ]
}
logger.configure(**logger_cfg)
print('Start logging to:', file_path)

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
