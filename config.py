import datetime
import os
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from loguru import logger
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from peewee import SqliteDatabase, PostgresqlDatabase

from db.settings import *
import psycopg2

#  определяем директорию проекта
BASE_DIR = Path(__file__).resolve().parent

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
with open(f"{BASE_DIR}/db/session.txt", 'r', encoding='utf-8') as f:
    SESSION_STRING = f.read()

# set admins list
me = os.getenv("ME_TELEGRAM_ID")
admins_list = [me]#, '305353027']
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
logger.remove()
logger.add(sink=file_path, enqueue=True, level=LOG_LEVEL, rotation="50 MB")
logger.add(sink=sys.stdout, level=DEBUG_LEVEL)
logger.configure(
    levels=[
        dict(name="DEBUG", color="<white>"),
        dict(name="INFO", color="<fg #afffff>"),
        dict(name="WARNING", color="<light-yellow>"),
        dict(name="ERROR", color="<red>"),
    ]
)
logger.info('Start logging to:', file_path)
#  ********** END OF LOGGER CONFIG *************************


#  ********** DATABASE CONFIG *************************

db_file_name = f'{BASE_DIR}/db/users.db'
def sqlite():
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
    return db


@logger.catch
def psql():
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    dbp = PostgresqlDatabase(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    dbp.connect()
    return dbp
db = sqlite()
#  ********** END OF DATABASE CONFIG *************************


#  *************** GETCOUSE API CONFIG ****************************

REQUEST_LIMIT = 5
KICK_RATE = kick_rate
REQUEST_RATE = admin_rate

#  ********** END OF GETCOUSE API  CONFIG *************************
