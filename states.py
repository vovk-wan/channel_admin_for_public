from aiogram.dispatcher.filters.state import State, StatesGroup
from config import logger


def get_state_name(state: State):
    return state.state.split(':')[-1]


class UserState(StatesGroup):
    """Машина состояний для управления пользователями."""
    wait_telephone_number = State()


class AdminState(StatesGroup):
    """Машина состояний для администратора."""
    # стартовое меню администратора
    start_admin = State(state='start_admin')
    # смена группы для листа ожидания
    waiting_group = State(state='waiting_group')
    # смена группы для членов группы
    club_group = State(state='club_group')
    # запись в баз новой группы
    edit_group = State(state='group_registration')
    # меню смены каналов
    edit_channel_list = State(state='edit_channel_list')
    # добавить канал
    add_channel = State(state='add_channel')
    # меню рассылки оплаты по листу ожидания
    mailing_list = State(state='mailing_list')
    # вернутся в пользовательское меню
    exit = State(state='exit')

    @classmethod
    def get_state_by_name(cls, state: str):
        try:
            return getattr(cls, state)
        except AttributeError as err:
            logger.info(err)
            return cls.start_admin


class MenuState(StatesGroup):
    """Machine state for menu"""
    start = State()  # основное меню
    about = State()  # нажал "о клубе"
    want = State()  # нажал "хочу в клуб"
    reviews = State()  # нажал "отзывы"
    prices = State()  # нажал "Тарифы"
    club_not_got_link = State()  # в клубе, в основном списке, ссылку не получал
    club_got_link = State()  # в клубе, в основном списке, ссылку получал
    excluded = State()  # в клубе был, продление не оплачено
    wait_list = State()  # не был в клубе, но есть в листе ожидания
    challenger = State()  # не был в клубе, нет в листе ожидания, есть телеграм ид в базе
    not_in_base = State()  # не был в клубе, или нет телеграм ид в базе

    @classmethod
    def get_state(cls, state: str):
        try:
            return getattr(cls, state)
        except AttributeError as err:
            logger.info(err)
            return cls.start
