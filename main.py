#!/usr/local/bin/python
"""
Python 3.9
Стартовый модуль
"""

import os.path
import datetime

import asyncio
from aiogram import executor

from config import dp, logger, bot, db_file_name, admins_list
from handlers.admin_menu import admin_menu_register_handlers
from handlers.user_menu import user_menu_register_handlers
from models import recreate_db
from scheduler_funcs import check_base, edit_group_list

user_menu_register_handlers(dp=dp)
admin_menu_register_handlers(dp=dp)


@logger.catch
async def send_report_to_admins(text: str) -> None:
    """Отправляет сообщение в телеграм всем администраторам из списка"""
    for admin_id in admins_list:
        try:
            await bot.send_message(chat_id=admin_id, text=text)
        except Exception as err:
            logger.error(err)


@logger.catch
async def on_startup(_) -> None:
    """Функция выполняющаяся при старте бота."""

    try:
        # Отправляет сообщение админам при запуске бота
        await send_report_to_admins(text="Бот запущен")
    except Exception:
        pass
    if not os.path.exists('./db'):
        os.mkdir("./db")
    if not os.path.exists(db_file_name):
        logger.warning(f"Database not found with file name: {db_file_name}")
        recreate_db(db_file_name)

    logger.info('Bot started at:', datetime.datetime.now())
    logger.info("BOT POLLING ONLINE")
    # edit_group_list()  # TODO включить в релизе
    # asyncio.create_task(check_base())  # TODO включить в релизе


@logger.catch
async def on_shutdown(dp) -> None:
    """Действия при отключении бота."""
    try:
        await send_report_to_admins(text="Бот остановлен")
    except Exception:
        pass
    logger.warning("BOT shutting down.")
    await dp.storage.wait_closed()
    logger.warning("BOT down.")


@logger.catch
def start_bot() -> None:
    """Инициализация и старт бота"""

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
    )


if __name__ == '__main__':
    start_bot()
