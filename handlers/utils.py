from typing import Union, List

from models import User, Statuses, Channel
from aiogram.types import Chat
from config import logger, bot


@logger.catch
def get_position(user: User) -> str:
    result = 'challenger'

    if user.status == Statuses.challenger:
        result = 'challenger'
    elif user.status in (
            Statuses.entered, Statuses.returned, Statuses.privileged) and user.got_invite:
        result = 'club_got_link'
    elif user.status in (
            Statuses.entered, Statuses.returned, Statuses.privileged) and not user.got_invite:
        result = 'club_not_got_link'
    elif user.status == Statuses.excluded:
        result = 'excluded'
    elif user.status == Statuses.waiting:
        result = 'wait_list'

    return result


@logger.catch
def get_user_position(telegram_id: int) -> str:
    """
    Запрашивает в каком списке находится пользователь вернуть строкой позицию    примерный выбор
    """
    user = User.get_users_by_telegram_id(telegram_id=telegram_id)
    if user:
        return get_position(user)

    return 'not_in_base'


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
    data = Channel.get_channels()

    channels = []
    for ch in data:
        try:
            result = await bot.get_chat(ch.channel_id)
            if result:
                channels.append(result)
        except Exception as err:
            logger.error(err)
    admins_name: tuple = await get_channel_admin(channels=channels)
    return admins_name
