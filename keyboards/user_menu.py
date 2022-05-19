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
def inline_button_link() -> InlineKeyboardButton:
    """Возвращает кнопку с инвайт ссылкой"""

    return InlineKeyboardButton(
        text='Получить ссылку', callback_data='start', url='https://google.ru')

# ***** end inline buttons ****************


@logger.catch
def start_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton(text='О клубе', callback_data='about'),
            inline_button_want(),
            InlineKeyboardButton(text='Тарифы', callback_data='prices'),
            InlineKeyboardButton(text='Отзывы', callback_data='reviews'),
    )


@logger.catch
def about_() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            inline_button_want(),
    )


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
def club_not_paid_() -> InlineKeyboardMarkup:

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
            inline_button_link(),
    )


@logger.catch
def challenger_() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        button_contact(),
        button_start(),
    )
