"""Модуль с клавиатурами и кнопками"""
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

from config import logger


@logger.catch
def cancel_keyboard() -> 'ReplyKeyboardMarkup':
    """Возвращает кнопку 'Отмена'"""

    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True).add(KeyboardButton("Отмена"))


@logger.catch
def admin_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton(text='Каналы/Группы', callback_data='channels'),
            InlineKeyboardButton(text='Геткурс группа', callback_data='group'),
            InlineKeyboardButton(text='Отправить ссылки на оплату', callback_data='отправляются ссылки'),
            InlineKeyboardButton(text='Редактировать текст', callback_data='edit_texts'),
            InlineKeyboardButton(text='Изменить лист ожидания', callback_data='непонятно что делать'),
    )
