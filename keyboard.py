"""Модуль с клавиатурами и кнопками"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from config import logger


@logger.catch
def cancel_keyboard() -> 'ReplyKeyboardMarkup':
    """Возвращает кнопку 'Отмена'"""

    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True).add(KeyboardButton("Отмена")
    )
