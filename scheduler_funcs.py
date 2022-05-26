from typing import List, Dict
import datetime
import asyncio

import aiogram.utils.exceptions
import aioschedule
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.storage import BaseStorage
from aiogram.types.chat import Chat
from aiogram.types import InlineKeyboardMarkup


import states
from config import bot, logger, EMOJI, REQUEST_LIMIT, REQUEST_RATE, KICK_RATE, admins_list
from get_channel_info import get_channel_data
from getcourse_requests import get_data, make_user_list_by_group, make_groups_list
from models import User, Channel, Group, Statuses, SourceData, GetcourseGroup, MessageNewStatus
from keyboards.admin import admin as keyboard_admin
from keyboards.user import make_keyboard_for_mailing


@logger.catch
async def send_message_to_admin(text: str, keyboard: InlineKeyboardMarkup = None) -> None:
    """Отправляет сообщение админам"""
    for admin_id in admins_list:
        try:
            await bot.send_message(
                chat_id=admin_id,
                text=text,
            )

        except Exception as err:
            logger.error(err)


async def mailing_new_status(users: list):
    """Отправляет сообщение пользователям о смене статуса"""
    messages: dict = MessageNewStatus.get_messages()
    for user in users:
        telegram_id = user.telegram_id
        text = messages.get(user.status, '').strip()
        if text:
            try:
                keyboard = make_keyboard_for_mailing(user.status, user.got_invite)
                await bot.send_message(chat_id=telegram_id, text=text, reply_markup=keyboard)
            except Exception as err:
                logger.error(f'{err.__traceback__.tb_frame}\n{err}')


@ logger.catch
def edit_group_list() -> int:
    """
    Получает список групп от API
    обновляет записи групп в DB
    :return:
    """
    groups = make_groups_list()
    if groups:
        return Group.edit_group(groups)
    logger.error('scheduler_funcs.edit_group_list not update')


@logger.catch
def get_data_id_from_api(group_id: str) -> int:
    """
    Запрашивает создание списка пользователей в группе от API
    :param group_id: id группы
    :return: возвращает id файла сформированного API
    """
    logger.debug('Starting checking ')
    response = make_user_list_by_group(group_id=group_id)
    if not response:

        logger.info('Data id not received.')
        return 0
    data_id, time_request = response
    logger.debug(' Data id received, requesting user data')

    return data_id


@logger.catch
async def get_data_from_api(data_id: int, source: str) -> list:
    """
    Получает данные пользователей с активной подпиской от API
    :param data_id: id файла сформированного API
    :param source:
    :return: список пользователей
    """
    data = await get_data(data_id, REQUEST_LIMIT, group_name=source)
    if data.get('error', True):
        logger.info(f'Data not received\n work stopped ')
        return []

    logger.debug(f'Data received')
    data_from_getcourse = data.get('data', [])

    return data_from_getcourse


@logger.catch
async def channel_exclude_users(data: list, channels: list) -> None:
    """
    FIXME test
    Удаляет пользователей с окончившейся подпиской из канала.
    Меняет статус пользователей на исключен
    :param data: список пользователей полученных от API.
    :param channels: список каналов которые бот администрирует.
    :return: None
    """
    getcourse_id = tuple(user.get('getcourse_id', None) for user in data)
    list_for_exclude = User.get_list_users_for_exclude(getcourse_id=getcourse_id)
    if list_for_exclude:
        for channel_data in channels:
            channel_id = channel_data.channel_id

            logger.info('List users for kicked received.\n Starting delete users for channel')
            channel: Chat = await bot.get_chat(channel_id)
            admins = await channel.get_administrators()
            admins_id = [str(user.user.id) for user in admins]
            count = 0
            for telegram_id in list_for_exclude:
                if telegram_id and telegram_id not in admins_id:
                    try:
                        await bot.kick_chat_member(channel_id, int(telegram_id))
                        count += 1
                    except aiogram.utils.exceptions.BadRequest as err:
                        logger.error(err)
            logger.info(
                f'Removed {count} users from the channel{channel_data.name} '
                f'\n list of telegram ids of kicked users: {list_for_exclude}')
    else:
        logger.info(f'{EMOJI.like} No users to delete')
    logger.debug('Starting delete users from DB')
    count = User.exclude_user_by_getcourse_id(list(getcourse_id))
    logger.info(f'{count}  users get status excluded')


@logger.catch
async def channel_kick_hackers(
        all_members: Dict[int, dict], all_users: List[int], channel_id: str) -> None:
    """
    FIXME удалять тех кто не в клубе то есть отсутствующих в базе и статус не в клубе
    Удаляет пользователей телеграм ид которых нет в базе из канала
    :param all_members: словарь членов канала где ключ telegram id
    значение словарь с  подробной информацией
    :param all_users:  список пользователей полученных от API
    :param channel_id: id канала который бот администрирует
    :return:
    """

    channel: Chat = await bot.get_chat(channel_id)
    admins = await channel.get_administrators()
    all_users.extend([user.user.id for user in admins])
    all_members_id: List[int] = list(all_members.keys())

    list_for_kicked: List[int] = [
        member for member in all_members_id
        if member not in all_users
    ]
    if not list_for_kicked:
        logger.info(f' No users to delete')
        return

    logger.info('List users for kicked received.\n Starting delete users for channel')
    count = 0
    for telegram_id in list_for_kicked:
        try:
            logger.info(f'kick: {telegram_id}')
            await bot.kick_chat_member(channel_id, telegram_id)
            count += 1
        except aiogram.utils.exceptions.BadRequest as err:
            member: dict = all_members.get(telegram_id, {'error': 'Не удалось получить данные'})
            text: str = 'Не удалось удалить пользователя:\n' + ''.join(
                [f'{key}: {value}\n'
                 for key, value in member.items()]
            )
            await send_message_to_admin(text=text)
            logger.error(err)

    logger.info(
        f'Removed {count} users from the channel '
        f'\n list of telegram ids of kicked users: {list_for_kicked}')


@logger.catch
def add_new_users(data: list, source: str) -> int:
    """
    обновляет пользователей
    :param data: список пользователей
    :param source: источник данных
    :return:
    """
    return User.update_users(users=data, source=source)


@logger.catch
async def channel_maintenance() -> None:
    """
    Функция обслуживания канала.
    :return:
    """

    logger.info(f'start channel maintenance: start')

    channels: list = Channel.get_channels()
    if not channels:
        await send_message_to_admin('Нет id канала, нужно добавить id канала и выбрать группу.\n'
                                    ' воспользуйтесь командой. \n/admin', keyboard_admin())

        logger.error('not channel_id. work stopped ')
        return
    edit_group_list()
    logger.info('get groups')

    member_group_id = GetcourseGroup.get_club_group()
    if not member_group_id:
        await send_message_to_admin('Нет id основной группы, нужно выбрать группу.\n'
                                    'воспользуйтесь командой.\n/admin', keyboard_admin())

        logger.error('not member_group_id. work stopped ')
        return

    logger.info('club group  get data')
    data_id = get_data_id_from_api(member_group_id)
    if not data_id:
        logger.error('not data_id. club group work stopped ')
        return
    data = await get_data_from_api(data_id, SourceData.club)

    if not data:
        logger.error('not user list. club group work stopped ')
        return

    logger.info(f'start channel maintenance: club group')
    await channel_exclude_users(data, channels)

    count = add_new_users(data, SourceData.club)
    logger.info(f'{count} users updated to BD club group')
    users_with_updated_status = User.get_users_for_mailing_new_status()
    await mailing_new_status(users_with_updated_status)
    count = User.un_set_status_updated_for_all()
    logger.info(f'{count} mail sends')

    waiting_group_id = GetcourseGroup.get_waiting_group()
    if not waiting_group_id:
        await send_message_to_admin('Нет id группы листа ожидания, нужно выбрать группу.\n'
                                    'воспользуйтесь командой.\n/admin')

        logger.error('not waiting_group_id. work stopped ')
        return

    logger.info('get data waiting list')
    data_id = get_data_id_from_api(waiting_group_id)
    if not data_id:
        logger.error('not data_id.  waiting list work stopped ')
        return
    data = await get_data_from_api(data_id, SourceData.waiting_list)

    if not data:
        logger.error('not user list.  waiting list work stopped ')
        return

    count = add_new_users(data, SourceData.waiting_list)
    logger.info(f'{count} users updated to BD waiting list group')
    getcourse_id = tuple(user.get('getcourse_id', None) for user in data)
    count = User.delete_user_from_waiting_list_by_getcourse_id(list(getcourse_id))
    logger.info(f'{count}  users delete from DB')
    await mailing_new_status(users_with_updated_status)
    count = User.un_set_status_updated_for_all()
    logger.info(f'{count} mail sends')


async def kick_hackers():
    """
    Функция для сбора данных и удаления из канала пользователей не записанных в базе
     как члены клуба
    кроме администраторов канала
    """
    logger.info(f'start kick_hackers: {datetime.datetime.utcnow()}')
    channels: list = Channel.get_channels()
    if not channels:
        logger.info('scheduler_func.kick_hackers: No channel')
        return

    all_users: List[int] = User.get_users_not_admins()
    for channel_data in channels:
        channel_id = channel_data.channel_id
        try:
            logger.info(f' try get_channel_data: {datetime.datetime.utcnow()}')
            logger.info('Get admins list')

            all_members: Dict = await get_channel_data(str(channel_id)[4:])

            await channel_kick_hackers(
                all_members=all_members, all_users=all_users, channel_id=channel_id)

        except Exception as err:
            logger.error(f' cannel name : {channel_data.name} {err}')
    logger.info(f' stop kick hackers: {datetime.datetime.utcnow()}')


@logger.catch
async def check_base():
    # aioschedule.every(REQUEST_RATE).minutes.do(channel_maintenance)
    # aioschedule.every(KICK_RATE).minutes.do(kick_hackers)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
