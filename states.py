from aiogram.dispatcher.filters.state import State, StatesGroup


class UserState(StatesGroup):
    """Машина состояний для управления пользователями."""
    wait_telephone_number = State()


class AdminState(StatesGroup):
    """Машина состояний для администратора."""
    channel_registration = State()
    group_registration = State()
