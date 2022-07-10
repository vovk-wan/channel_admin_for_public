from dataclasses import dataclass
from typing import Callable

from config import logger
# from models import Text
from services import APITextInterface


@dataclass
class TextsUser:
    #  Приветственное сообщение Основное меню
    start: Callable = APITextInterface.get_start_text

    # Текст о клубе
    about: Callable = APITextInterface.get_about_text

    # Текст Прайс
    prices: Callable = APITextInterface.get_prices_text

    # Отзывы
    reviews: Callable = APITextInterface.get_reviews_text

    # Текст после хочу в клуб если нет в базе телеграм ид
    not_in_base: Callable = APITextInterface.get_want_for_get_phone_text

    # Текст после хочу в клуб, но в базе только как претендент
    challenger: Callable = APITextInterface.get_want_for_challenger_text

    # Текст после хочу в клуб если оплатил в клубе и не получал ссылку
    club_not_got_link: Callable = APITextInterface.get_want_for_entered_text

    # Текст после хочу в клуб, уже оплатил уже в клубе, но получал ссылку
    club_got_link: Callable = APITextInterface.get_want_for_entered_got_link_text

    # Текст после хочу в клуб если не оплатил, но был уже в клубе
    excluded: Callable = APITextInterface.get_want_for_excluded_text

    # Текст если есть в листе ожидания
    wait_list: Callable = APITextInterface.get_want_for_waiting_list_text

    # Текст сопровождение со ссылкой
    get_invite_link: Callable = APITextInterface.get_for_invite_text

    @classmethod
    @logger.catch
    def get_menu_text(cls, name: str):
        try:
            return getattr(cls, name)
        except AttributeError as err:
            logger.info(f'{cls.__qualname__} exception: {err}')
            return cls.start


@dataclass
class AdminTexts:
    """Тексты в меню администратора"""
    #  текст стартового меню администраторов
    start_admin: str = lambda: "Меню администратора"

    # изменение группы листа ожидания
    waiting_group: str = lambda: 'Меняем группу Waiting list'

    # изменение группы для членов клуба
    club_group: str = lambda: 'Меняем основную группу членов клуба'

    # изменение каналов
    edit_channel_list: str = lambda: 'Удалить или добавить каналы - группы'

    # изменение каналов
    add_channel: str = lambda: ('Чтобы добавить новый канал нужно ввести его id \n'
                                'или вставить ссылку на любое сообщение в канале ')

    # рассылка ссылок на оплату
    mailing_list: str = lambda: ('Введите текст или ссылку для отправки сообщения '
                                 'всем пользователям в листе ожидания')

    @classmethod
    @logger.catch
    def get_menu_text(cls, name: str):
        try:
            return getattr(cls, name)
        except AttributeError as err:
            logger.info(f'{cls.__qualname__} exception: {err}')
            return cls.start_admin
