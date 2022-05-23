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
def admin_menu() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton(text='Каналы/Группы', callback_data='edit_channel_list'),
            InlineKeyboardButton(text='Геткурс группа', callback_data='club_group'),
            InlineKeyboardButton(text='Отправить ссылки на оплату', callback_data='mailing_list'),
            # InlineKeyboardButton(text='Редактировать текст', callback_data='edit_texts'),
            InlineKeyboardButton(text='Изменить лист ожидания', callback_data='waiting_group'),
            InlineKeyboardButton(text='Назад', callback_data='start_admin'),
            InlineKeyboardButton(text='Выход', callback_data='user_menu'),
    )


@logger.catch
def add_channel() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='Отмена', callback_data='edit_channel_list')
    )
