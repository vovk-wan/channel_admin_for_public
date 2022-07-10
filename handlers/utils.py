import datetime
from functools import wraps
from typing import Union, List, Callable, Any

from models import Statuses
# from models import User, Statuses, Channel
from aiogram.types import Chat, Message
from config import logger, bot
from services import APIUsersInterface, APIChannelsInterface


@logger.catch
def get_position(user: dict) -> str:
    result = 'challenger'

    if user.get('status') == Statuses.challenger:
        result = 'challenger'
    elif user.get('status') in (
            Statuses.entered, Statuses.returned, Statuses.privileged) and user.get('got_invite'):
        result = 'club_got_link'
    elif user.get('status') in (
            Statuses.entered, Statuses.returned, Statuses.privileged) and not user.get('got_invite'):
        result = 'club_not_got_link'
    elif user.get('status') == Statuses.excluded:
        result = 'excluded'
    elif user.get('status') == Statuses.waiting:
        result = 'wait_list'

    return result


@logger.catch
def get_user_position(telegram_id: int) -> str:
    """
    Запрашивает в каком списке находится пользователь вернуть строкой позицию    примерный выбор
    """
    user = APIUsersInterface.get_users_by_telegram_id(telegram_id=telegram_id)
    if user.get('status'):
        return get_position(user)

    return 'not_in_base'


@logger.catch
def get_user_access(telegram_id: int) -> bool:
    """
    Возвращает доступ пользователя к каналам и группам
    """
    access = False
    user = APIUsersInterface.get_users_by_telegram_id(telegram_id=telegram_id)
    if user:
        month = datetime.datetime.strptime(user.get('date_joining_club'), "%Y-%m-%dT%H:%M:%S").month
        access = month < datetime.datetime.now().month
    return access


@logger.catch
async def get_channel_admin(channels: Union[Chat, List[Chat]]) -> tuple:
    """Function returned channel admin name"""

    if isinstance(channels, Chat):
        channels = [channels]

    admins_name: set = set()
    for channel in channels:
        try:

            admins = await channel.get_administrators()
            for admin in admins:
                if not admin.user.is_bot:
                    admins_name.add(admin.user.mention)

        except Exception as err:
            logger.error(err)

    return tuple(admins_name)


@logger.catch
async def get_all_admins() -> tuple:
    """Function returned all admins for saved channel"""
    data = APIChannelsInterface.get_channels()

    channels = []
    for ch in data:
        try:
            result = await bot.get_chat(ch.get('channel_id'))
            if result:
                channels.append(result)
        except Exception as err:
            logger.error(err)
    admins_name: tuple = await get_channel_admin(channels=channels)
    return admins_name


@logger.catch
def check_message_private(func: Callable) -> Callable:
    """decorator for handler check message is private"""

    @wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        message: Message = args[0]
        message_chat_id = message.from_user.id
        chat_id = message.chat.id
        if message_chat_id == chat_id:
            logger.debug(f"Message {message_chat_id} == {chat_id}.")
            return await func(*args, **kwargs)
        logger.debug(f"Message {message_chat_id} != {chat_id}.")

    return wrapper
