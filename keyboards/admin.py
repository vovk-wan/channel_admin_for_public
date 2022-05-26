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
def admin_menu(*args, **kwargs) -> InlineKeyboardMarkup:

    keyboard_menu = InlineKeyboardMarkup(row_width=1)

    keyboard_menu.add(
        InlineKeyboardButton(text='изменить основную группу', callback_data='club_group'),
        InlineKeyboardButton(text='Изменить лист ожидания', callback_data='waiting_group'),
        InlineKeyboardButton(text='Отправить ссылки на оплату', callback_data='mailing_list'),
        InlineKeyboardButton(text='Каналы/Группы', callback_data='edit_channel_list'),
        InlineKeyboardButton(text='Выход', callback_data='exit'),
    )
    # InlineKeyboardButton(text='Редактировать текст', callback_data='edit_texts'),
    return keyboard_menu


@logger.catch
def cancel_edit_channel(*args, **kwargs) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='Отмена', callback_data='edit_channel_list')
    )


@logger.catch
def cancel(*args, **kwargs) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='Отмена', callback_data='about')
    )


@logger.catch
def admin(*args, **kwargs) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton(text='admin', callback_data='start_admin')
    )
