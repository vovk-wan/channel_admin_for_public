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
    start = State(state='start')  # основное меню
    about = State(state='about')  # нажал "о клубе"
    want = State(state='want')  # нажал "хочу в клуб"
    reviews = State(state='reviews')  # нажал "отзывы"
    prices = State(state='prices')  # нажал "Тарифы"
    club_not_got_link = State(state='club_not_got_link')  # в клубе, ссылку не получал
    club_got_link = State(state='club_got_link')  # в клубе, в основном списке, ссылку получал
    excluded = State(state='excluded')  # в клубе был, продление не оплачено
    wait_list = State(state='wait_list')  # не был в клубе, но есть в листе ожидания
    challenger = State(state='challenger')  # не был в клубе, нет в листе ожидания, есть  базе
    not_in_base = State(state='not_in_base')  # не был в клубе, или нет телеграм ид в базе
    get_invite_link = State(state='get_invite_link')  # получить ссылку

    @classmethod
    def get_state(cls, state: str):
        try:
            return getattr(cls, state)
        except AttributeError as err:
            logger.info(err)
            return cls.start
