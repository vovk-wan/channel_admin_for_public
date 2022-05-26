"""Модуль с клавиатурами и кнопками"""
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

from config import logger
from models import Text


@logger.catch
def cancel_keyboard() -> 'ReplyKeyboardMarkup':
    """Возвращает кнопку 'Отмена'"""

    return ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True).add(KeyboardButton("Отмена"))


#  *********** buttons ****************

@logger.catch
def button_contact() -> KeyboardButton:
    """Возвращает кнопку 'Отправить контакт'"""
    return KeyboardButton(text='Отправить контакт', request_contact=True, )


@logger.catch
def button_start() -> KeyboardButton:
    """Возвращает кнопку 'Меню'"""

    return KeyboardButton(text='Назад')

#  ********** end buttons ***************


#  ***** inline buttons ****************

@logger.catch
def inline_button_cancel() -> InlineKeyboardButton:
    """Возвращает кнопку 'Отмена'"""

    return InlineKeyboardButton(text='Отмена', callback_data='cancel')


@logger.catch
def inline_button_want() -> InlineKeyboardButton:
    """Возвращает кнопку 'Хочу в клуб'"""

    return InlineKeyboardButton(text='Хочу в клуб', callback_data='want')


@logger.catch
def inline_button_start() -> InlineKeyboardButton:
    """Возвращает кнопку 'Меню'"""

    return InlineKeyboardButton(text='Назад', callback_data='start')


@logger.catch
def inline_button_invite_link() -> InlineKeyboardButton:
    """Возвращает кнопку с инвайт ссылкой"""

    return InlineKeyboardButton(
        text='Получить ссылку', callback_data='get_invite_link')


@logger.catch
def inline_button_link_wait_list() -> InlineKeyboardButton:
    """Возвращает кнопку с инвайт ссылкой"""
    url = Text.get_link_waiting_list_text()
    return InlineKeyboardButton(
        text='Ссылка на лист ожидания ', callback_data='start', url=url)

# ***** end inline buttons ****************


@logger.catch
def start_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=3).add(
        inline_button_want(),
        InlineKeyboardButton(text='О клубе', callback_data='about'),
        InlineKeyboardButton(text='Тарифы', callback_data='prices'),
        InlineKeyboardButton(text='Отзывы', callback_data='reviews'),
    )


@logger.catch
def about_() -> InlineKeyboardMarkup:

    about_keyboard = InlineKeyboardMarkup()
    about_keyboard.row(inline_button_start(), inline_button_want(),)
    return about_keyboard


@logger.catch
def want_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            inline_button_want(),
    )


@logger.catch
def paid_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            InlineKeyboardButton(text='Получить инвайт ссылку', callback_data='invite'),
    )


@logger.catch
def excluded_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            InlineKeyboardButton(text='Ссылка на оплату', callback_data='скорее всего просто ссылка'),
    )


@logger.catch
def contact_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            InlineKeyboardButton(text='Ссылка на лист ожидания', callback_data='wait_list'),
    )


@logger.catch
def link_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            inline_button_invite_link(),
    )


@logger.catch
def challenger_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            inline_button_link_wait_list(),
    )


@logger.catch
def not_in_base_() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        button_contact(),
        button_start(),
    )


@logger.catch
def club_got_link_() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(inline_button_start())


@logger.catch
def wait_list_() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(inline_button_start())
