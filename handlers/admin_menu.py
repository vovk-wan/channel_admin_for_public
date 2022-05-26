"""Модуль с основными обработчиками команд, сообщений и нажатия inline кнопок"""
from dataclasses import dataclass

import aiogram.utils.exceptions
from aiogram.dispatcher import FSMContext
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton, ReplyKeyboardRemove)
from aiogram.types.chat import Chat

from config import logger, bot, admins_list
from keyboards import admin
from models import GetcourseGroup, Channel, User, Text
from models import Group
from scheduler_funcs import mailing_new_status
from states import AdminState, get_state_name
from texts.menu import AdminTexts
from keyboards.user import link_menu


@dataclass
class AdminKeyboard:
    """keyboards"""
    start_admin: InlineKeyboardMarkup = admin.admin_menu
    waiting_group: InlineKeyboardMarkup = admin.admin_menu
    club_group: InlineKeyboardMarkup = admin.admin_menu
    edit_channel_list: InlineKeyboardMarkup = admin.admin_menu
    mailing_list: InlineKeyboardMarkup = admin.cancel
    user_menu: InlineKeyboardMarkup = admin.admin_menu
    add_channel: InlineKeyboardMarkup = admin.cancel_edit_channel

    @classmethod
    def get_menu_keyboard(cls, name: str):
        try:
            return getattr(cls, name)
        except AttributeError as err:
            logger.info(err)
            return cls.user_menu


async def start_menu_admin(callback: CallbackQuery, state: FSMContext) -> None:
    """ Admin menu"""
    name_state = callback.data
    chat_id = callback.message.chat.id
    group_id = GetcourseGroup.get_club_group()
    club_group_name = Group.get_name_group_by_id(group_id)
    groups = f'\nтекущая группа членов клуба "{club_group_name}-{group_id}'
    group_id = GetcourseGroup.get_waiting_group()
    waiting_group_name = Group.get_name_group_by_id(group_id)
    groups += f'\nтекущая группа для листа ожидания "{waiting_group_name}-{group_id}'
    channel_names = Channel.get_channels()
    channel_list = "\n".join(f'{channel.name} - {channel.channel_id}' for channel in channel_names)
    channels = f'\n\nтекущие каналы \n {channel_list}'

    text = AdminTexts.get_menu_text(name_state)()
    text = text + groups + channels
    keyboard = AdminKeyboard.get_menu_keyboard(name_state)()

    data = await state.get_data()
    start_message = data.get('start_message')

    try:
        await bot.edit_message_text(
            text=text, chat_id=chat_id, message_id=start_message, reply_markup=keyboard)

    except (aiogram.utils.exceptions.MessageNotModified,
            aiogram.utils.exceptions.MessageCantBeEdited) as err:
        logger.error(err)

        mess = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
        await state.update_data(start_message=mess.message_id)


@logger.catch
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Ставит все State в нерабочее состояние.
    Обработчик команды /cancel
    """
    await message.answer(
        "Вы отменили текущую команду.",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.finish()


@logger.catch
async def return_telegram_id_handler(message: Message) -> None:
    """Функция возвращает пользователю его id telegram"""
    await message.answer(f'user id: {message.from_user.id}')


@logger.catch
async def group_registration(callback: CallbackQuery, state: FSMContext) -> None:
    """Функция запроса изменения группы для получения списка пользователей с 'API'"""
    telegram_id = callback.from_user.id
    if str(telegram_id) in admins_list:
        groups = Group.get_all_group_channel()
        keyboard_group: 'InlineKeyboardMarkup' = InlineKeyboardMarkup(row_width=1)
        for button in groups:
            keyboard_group.add(
                InlineKeyboardButton(text=f'{button[1]}', callback_data=f'{button[0]}'))
        keyboard_group.add(InlineKeyboardButton(text='Отмена', callback_data='start_admin'))
        name_state = callback.data
        chat_id = callback.message.chat.id

        data = await state.get_data()
        text = AdminTexts.get_menu_text(name_state)()

        start_message = data.get('start_message')
        current_state = callback.data
        await state.set_state(AdminState.edit_group)
        await state.update_data({'group_edit': current_state})
        try:
            await bot.edit_message_text(
                text=text, chat_id=chat_id, message_id=start_message, reply_markup=keyboard_group)

        except aiogram.utils.exceptions.MessageNotModified as err:
            logger.error(err)
        await callback.answer()


@logger.catch
async def edit_group(callback: CallbackQuery, state: FSMContext) -> None:
    """Функция производит изменение id группы для получения списка пользователей с 'API'"""
    telegram_id = callback.from_user.id
    if str(telegram_id) in admins_list:
        data = await state.get_data()
        group_edit = data.get('group_edit')

        answer = 'Группа не изменена'
        new_state = get_state_name(AdminState.start_admin)

        if group_edit == get_state_name(AdminState.club_group) and callback.data != new_state:
            GetcourseGroup.edit_club_group(callback.data)
            answer = 'Изменена группа членов клуба'
        elif group_edit == get_state_name(AdminState.waiting_group) and callback.data != new_state:
            GetcourseGroup.edit_waiting_group(callback.data)
            answer = 'Изменена группа листа ожидания'

        await bot.answer_callback_query(
            callback_query_id=callback.id, text=answer, show_alert=False)

        data.pop('group_edit')
        callback.data = new_state
        await state.update_data(data)
        await state.set_state(AdminState.start_admin)
        await start_menu_admin(callback, state)
        await callback.answer()


@logger.catch
async def channel_registration(callback: CallbackQuery, state: FSMContext) -> None:
    """Функция для управления каналами и группами, которыми бот должен управлять"""

    telegram_id = callback.from_user.id
    if str(telegram_id) in admins_list:
        name_state = callback.data
        if name_state == 'return':
            await callback.answer()
            return
        elif name_state == 'stop_edit_channel':
            await state.set_state(AdminState.start_admin)
            callback.data = get_state_name(AdminState.start_admin)
            await start_menu_admin(callback=callback, state=state)
            await callback.answer()
            return
        elif name_state == 'add_channel':
            await wait_text(callback=callback, state=state)
            await callback.answer()
            return
        elif name_state.split(':')[0] == 'delete':
            try:
                channel_id = name_state.split(':')[-1]
                Channel.delete_channel(int(channel_id))
                answer = "Канал уделен"
            except Exception as err:
                answer = 'Канал не уделен'
                logger.error(err)
            await bot.answer_callback_query(
                callback_query_id=callback.id, text=answer, show_alert=True)
            name_state = get_state_name(AdminState.edit_channel_list)

        channels = Channel.get_channels()
        keyboard_group: 'InlineKeyboardMarkup' = InlineKeyboardMarkup()
        for channel in channels:
            keyboard_group.row(
                InlineKeyboardButton(text=f'{channel.name}', callback_data='return'),
                InlineKeyboardButton(text='удалить', callback_data=f'delete:{channel.channel_id}')
            )
        keyboard_group.row(
            InlineKeyboardButton(text='Добавить', callback_data='add_channel'),
            InlineKeyboardButton(text='Закончить', callback_data='stop_edit_channel'))

        data = await state.get_data()
        chat_id = callback.message.chat.id
        text = AdminTexts.get_menu_text(name_state)()
        result_add_channel = data.get('result_add_channel')
        if result_add_channel:
            data.pop('result_add_channel')
            await state.set_data(data)

        start_message = data.get('start_message')
        try:
            await bot.edit_message_text(
                text=text, chat_id=chat_id,
                message_id=start_message,
                reply_markup=keyboard_group
            )

        except aiogram.utils.exceptions.MessageNotModified as err:
            logger.error(err)


@logger.catch
async def wait_text(callback: CallbackQuery, state: FSMContext) -> None:
    """Функция для ожидания текстового сообщения"""

    telegram_id = callback.from_user.id
    if str(telegram_id) in admins_list:
        data = await state.get_data()
        chat_id = callback.message.chat.id
        name_state = callback.data
        text = AdminTexts.get_menu_text(name_state)()
        start_message = data.get('start_message')
        keyboard = AdminKeyboard.get_menu_keyboard(name_state)()
        try:
            await bot.edit_message_text(
                text=text, chat_id=chat_id,
                message_id=start_message,
                reply_markup=keyboard
            )

        except aiogram.utils.exceptions.MessageNotModified as err:
            logger.error(err)
        await callback.answer()


@logger.catch
async def edit_channel(message: Message, state: FSMContext) -> None:
    """Функция производит изменение id канала для управления"""
    value: str = message.text
    channel_id = 0
    answer = 'Канал не найден попробуйте ещё раз'
    title = ''
    try:
        channel_id = int('-100' + value)
    except ValueError as err:
        logger.info(err)
    await message.delete()
    try:
        if not channel_id:
            value = '-100' + value.split('/')[-2]
            channel_id = int(value)
        channel: Chat = await bot.get_chat(channel_id)
        title = channel.title
        if not channel:
            raise ValueError('channel not found')
    except Exception as err:
        logger.error(err)
        channel_id = None

    callback = CallbackQuery()
    callback.message = message
    callback.id = message.message_id
    callback.from_user = message.from_user
    callback.data = get_state_name(AdminState.edit_channel_list)

    if channel_id:
        Channel.add_channel(channel_id=channel_id, channel_name=title)
        answer = 'Канал добавлен'
    await state.update_data(result_add_channel=answer)
    await channel_registration(callback=callback, state=state)


@logger.catch
async def mailing_list() -> int:
    """
    Функция отправляет ссылки на оплату всем
    пользователям из листа ожидания у кого есть телеграм ид
    """
    value: str = Text.get_link_paid_waiting_list()

    users = User.get_users_from_waiting_list()
    count = 0
    await mailing_new_status([User.get_users_by_telegram_id(5250931805)])
    # for telegram_id in users:
    #     try:
    #         await bot.send_message(telegram_id, value, reply_markup=link_menu())
    #         count += 1
    #     except Exception as err:
    #         logger.error(err)
    #
    # return count

    # callback = CallbackQuery()
    # callback.message = message
    # callback.id = message.message_id
    # callback.from_user = message.from_user
    # callback.data = get_state_name(AdminState.edit_channel_list)
    #
    # await start_menu_admin(callback=callback, state=state)
