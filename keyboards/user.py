"""Модуль с клавиатурами и кнопками"""
import aiogram.utils.exceptions
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

from config import logger
from models import Text
from handlers.utils import get_user_position
from models import Statuses


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
        text='Получить инвайт', callback_data='get_invite_link')


@logger.catch
def inline_button_link_user_menu() -> InlineKeyboardButton:
    """Возвращает кнопку со ссылкой на основное меню"""

    return InlineKeyboardButton(text='Menu', callback_data='get_user_menu')


@logger.catch
def inline_button_link_wait_list() -> InlineKeyboardButton:
    """Возвращает кнопку с инвайт ссылкой на лист ожидания"""
    url = Text.get_link_waiting_list_text()
    return InlineKeyboardButton(
        text='Ссылка на лист ожидания ', callback_data='start', url=url)

# ***** end inline buttons ****************


@logger.catch
def start_(*args, **kwargs) -> InlineKeyboardMarkup:
    """
        Возвращает клавиатуру основного меню
    """

    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3).add(
                                       inline_button_want(),
                                       InlineKeyboardButton(text='О клубе', callback_data='about'),
                                       InlineKeyboardButton(text='Тарифы', callback_data='prices'),
                                       InlineKeyboardButton(text='Отзывы', callback_data='reviews'),
                                    )
    telegram_id = kwargs.get('telegram_id')
    if get_user_position(telegram_id=telegram_id) == 'club_not_got_link':
        keyboard.add(inline_button_invite_link())
    return keyboard


@logger.catch
def about_(*args, **kwargs) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup()
    keyboard.row(inline_button_start(), inline_button_want(),)
    return keyboard


@logger.catch
def link_pay_waiting_list_menu(*args, **kwargs) -> InlineKeyboardMarkup:
    url: str = Text.get_link_to_pay()
    try:
        keyboard = InlineKeyboardMarkup().add(
            inline_button_link_user_menu(),
            InlineKeyboardButton(text='Ссылка на оплату', callback_data='get_user_menu', url=url),
        )
    except aiogram.utils.exceptions.ButtonURLInvalid as err:
        logger.error(err)
        keyboard = InlineKeyboardMarkup().add(
            inline_button_link_user_menu(),
            InlineKeyboardButton(text='Произошла ошибка', callback_data='get_user_menu'),
        )
    return keyboard


@logger.catch
def want_(*args, **kwargs) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            inline_button_want(),
    )


@logger.catch
def excluded_(*args, **kwargs) -> InlineKeyboardMarkup:
    """TODO добавить ссылку на оплату """
    url: str = Text.get_link_to_pay()

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            InlineKeyboardButton(text='Ссылка на оплату', callback_data='start', url=url),
    )


@logger.catch
def link_(*args, **kwargs) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            inline_button_invite_link(),
    )


@logger.catch
def challenger_(*args, **kwargs) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            inline_button_link_wait_list(),
    )


@logger.catch
def not_in_base_(*args, **kwargs) -> ReplyKeyboardMarkup:

    return ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
        button_contact(),
        button_start(),
    )


@logger.catch
def club_got_link_(*args, **kwargs) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(inline_button_start())


@logger.catch
def wait_list_(*args, **kwargs) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(row_width=1).add(inline_button_start())


@logger.catch
def make_keyboard_for_mailing(status: str, got_invite: bool) -> InlineKeyboardMarkup:
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=2)
    keyboard.add(inline_button_link_user_menu())
    if (status in [Statuses.entered, Statuses.returned, Statuses.privileged]
        and not got_invite):
        button = inline_button_invite_link()
        button.callback_data = 'get_invite_link_from_mailing'
        keyboard.add(button)
    elif status in [Statuses.excluded]:
        keyboard.add(inline_button_want())

    return keyboard
