"""Модуль с клавиатурами и кнопками"""
import aiogram.utils.exceptions
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)

from config import logger
# from models import Text
from handlers.utils import get_user_position, get_user_access
from models import Statuses
from services import APITextInterface


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
        text='Получить пригласительную ссылку', callback_data='get_invite_link')


@logger.catch
def inline_button_link_user_menu() -> InlineKeyboardButton:
    """Возвращает кнопку со ссылкой на основное меню"""

    return InlineKeyboardButton(text='Меню', callback_data='get_user_menu')


@logger.catch
def inline_button_link_wait_list() -> InlineKeyboardButton:
    """Возвращает кнопку с инвайт ссылкой на лист ожидания"""
    url = APITextInterface.get_link_waiting_list_text()
    return InlineKeyboardButton(
        text='Ссылка на лист ожидания', callback_data='start', url=url)

# ***** end inline buttons ****************


@logger.catch
def start_(*args, **kwargs) -> InlineKeyboardMarkup:
    """
        Возвращает клавиатуру основного меню
    """

    keyboard = InlineKeyboardMarkup()
    telegram_id = kwargs.get('telegram_id')
    if (get_user_position(telegram_id=telegram_id) == 'club_not_got_link' and
            get_user_access(telegram_id=telegram_id)):
        keyboard.row(inline_button_invite_link())
    keyboard.row(inline_button_want(),)
    keyboard.row(
        InlineKeyboardButton(text='Отзывы', callback_data='reviews'),
        InlineKeyboardButton(text='О клубе', callback_data='about'),
        InlineKeyboardButton(text='Тарифы', callback_data='prices'),
    )

    # keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=3).add(
    #                                    inline_button_want(),
    #                                    InlineKeyboardButton(text='О клубе', callback_data='about'),
    #                                    InlineKeyboardButton(text='Тарифы', callback_data='prices'),
    #                                    InlineKeyboardButton(text='Отзывы', callback_data='reviews'),
                                    # )

    return keyboard


@logger.catch
def about_(*args, **kwargs) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup()
    keyboard.row(inline_button_start(), inline_button_want(),)
    return keyboard


@logger.catch
def link_pay_waiting_list_menu(url: str) -> InlineKeyboardMarkup:
    # url: str = APITextInterface.get_link_to_pay()
    try:
        keyboard = InlineKeyboardMarkup().row(
            inline_button_link_user_menu(),
            InlineKeyboardButton(text='Ссылка на оплату', callback_data='get_user_menu', url=url),
        )
    except aiogram.utils.exceptions.ButtonURLInvalid as err:
        logger.error(err)
        keyboard = InlineKeyboardMarkup().row(
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
    """keyboard for excluded users """
    url: str = APITextInterface.get_link_to_pay()

    return InlineKeyboardMarkup(row_width=2).add(
            inline_button_start(),
            InlineKeyboardButton(text='Ссылка на оплату', callback_data='start', url=url),
    )


@logger.catch
def link_(*args, **kwargs) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    telegram_id = kwargs.get('telegram_id')
    if (get_user_position(telegram_id=telegram_id) == 'club_not_got_link' and
            get_user_access(telegram_id=telegram_id)):
        keyboard.row(inline_button_invite_link())
    keyboard.row(
        inline_button_start(),
    )

    return keyboard


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
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
    if status in [Statuses.entered, Statuses.returned, Statuses.privileged] and not got_invite:
        button = inline_button_invite_link()
        button.callback_data = 'get_invite_link_from_mailing'
        keyboard.row(button)
    elif status in [Statuses.excluded]:
        button = inline_button_want()
        button.callback_data = 'get_user_menu_want'
        keyboard.row(button)
    keyboard.row(inline_button_link_user_menu())

    return keyboard
