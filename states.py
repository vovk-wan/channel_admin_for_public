from aiogram.dispatcher.filters.state import State, StatesGroup
from config import logger


class UserState(StatesGroup):
    """Машина состояний для управления пользователями."""
    wait_telephone_number = State()


class AdminState(StatesGroup):
    """Машина состояний для администратора."""
    channel_registration = State()
    group_registration = State()


class MenyState(StatesGroup):
    """Machine state for menu"""
    start = State()  # основное меню
    about = State()  # нажал "о клубе"
    want = State()  # нажал "хочу в клуб"
    reviews = State()  # нажал "отзывы"
    prices = State()  # нажал "Тарифы"
    club_not_got_link = State()  # в клубе, в основном списке, ссылку не получал
    club_got_link = State()  # в клубе, в основном списке, ссылку получал
    club_not_paid = State()  # в клубе был, продление не оплачено
    wait_list = State()  # не был в клубе, но есть в листе ожидания
    challenger = State()  # не был в клубе, или нет телеграм ид в базе

    @classmethod
    def get_state(cls, state: str):
        try:
            return getattr(cls, state)
        except AttributeError as err:
            logger.info(f'{cls.__qualname__} exception: {err}')
            return cls.start
