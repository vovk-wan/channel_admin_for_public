"""Модуль с основными обработчиками команд, сообщений и нажатия inline кнопок"""
from dataclasses import dataclass

import aiogram.utils.exceptions
from aiogram.dispatcher.filters import Text
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton, ReplyKeyboardRemove)
from aiogram.types.chat import Chat

from aiogram.dispatcher import FSMContext

import states
from keyboards.admin import cancel_keyboard
from config import logger, Dispatcher, bot, EMOJI, admins_list
from models import Group, Channel
from states import AdminState, MenuState, get_state_name
from keyboards import admin
from models import GetcourseGroup, Channel

@dataclass
class AdminTexts:
    """TODO Заменить на запросы к бд"""
    #  текст стартового админского меню
    start_admin: str = "hello admin"

    # изменение группы листа ожидания
    waiting_group: str = 'Текст изменение группы листа ожидания'

    # изменение группы для членов клуба
    club_group: str = 'Текст изменение группы членов клуба'

    # изменение каналов
    edit_channel_list: str = 'Текст изменение списка каналов'

    # изменение каналов
    add_channel: str = 'Текст добавить новый канал'

    # рассылка ссылок на оплату
    mailing_list: str = 'Текст изменение каналов'

    @classmethod
    @logger.catch
    def get_menu_text(cls, name: str):
        try:
            return getattr(cls, name)
        except AttributeError as err:
            logger.info(f'{cls.__qualname__} exception: {err}')
            return cls.start_admin


@dataclass
class AdminKeyboard:
    """keyboards"""
    start_admin: InlineKeyboardMarkup = admin.admin_menu()
    waiting_group: InlineKeyboardMarkup = admin.admin_menu()
    club_group: InlineKeyboardMarkup = admin.admin_menu()
    edit_channel_list: InlineKeyboardMarkup = admin.admin_menu()
    mailing_list: InlineKeyboardMarkup = admin.admin_menu()
    user_menu: InlineKeyboardMarkup = admin.admin_menu()
    add_channel: InlineKeyboardMarkup = admin.add_channel()

    @classmethod
    def get_menu_keyboard(cls, name: str):
        try:
            return getattr(cls, name)
        except AttributeError as err:
            logger.info(err)
            return cls.user_menu

# @logger.catch
# async def cancel_handler(message: Message, state: FSMContext) -> None:
#     """
#     Ставит все состояния в нерабочие.
#     Обработчик команды /cancel
#     """
#     await state.finish()
#     await admin_start_handler(message, state=state)


@logger.catch
async def admin_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция промежуточная
    """
    telegram_id = callback.from_user.id
    chat_id = callback.message.chat.id
    name_state = callback.data
    new_state = AdminState.get_state_by_name(name_state)
    await state.set_state(new_state)

    if name_state in [
        get_state_name(AdminState.waiting_group), get_state_name(AdminState.club_group)
    ]:
        await group_registration(callback, state)
        return

    if name_state == get_state_name(AdminState.edit_channel_list):
        await channel_registration(callback, state)
        return

    group_id = GetcourseGroup.get_club_group()
    group_name = Group.get_name_group_by_id(group_id)
    groups = f'\nтекущая группа членов клуба "{group_name}'
    group_id = GetcourseGroup.get_waiting_group()
    group_name = Group.get_name_group_by_id(group_id)
    groups += f'\nтекущая группа для листа ожидания "{group_name}'
    channel_names = Channel.get_channels()
    channel_list = "\n".join(f'{channel.name} - {channel.channel_id}' for channel in channel_names)
    channels = f'\n\nтекущие каналы \n {channel_list}'

    text = AdminTexts.get_menu_text(name_state)
    text = text + groups + channels
    keyboard = AdminKeyboard.get_menu_keyboard(name_state)

    data = await state.get_data()
    start_message = data.get('start_message')
    additional_text = data.get('text', '')
    if additional_text:
        text = f'{additional_text}\n\n{text}'
        data.pop('text')
        await state.set_data(data)

    if not start_message:
        # TODO заполнить проверить все варианты
        logger.debug('deleted start menu')
        return

    try:
        await bot.edit_message_text(
            text=text, chat_id=chat_id, message_id=start_message, reply_markup=keyboard)

    except aiogram.utils.exceptions.MessageNotModified as err:
        logger.error(err)


@logger.catch
async def admin_handler(message: Message, state: FSMContext) -> None:
    user_id = message.from_user.id
    if str(user_id) in admins_list:
        await state.finish()
        channel_id = Channel.get_channel()
        channel_name = 'Нет данных'
        group_name = 'Нет данных'
        if channel_id:
            channel: Chat = await bot.get_chat(channel_id)
            channel_name = channel.full_name
        group_id = Channel.get_group()
        if group_id:
            group_name = Group.get_name_group_by_id(group_id)
        await message.answer(f'Команды администратора\n'
                             f'изменить канал текущий канал "{channel_name}"\n'
                             f'/channel\n'
                             f'изменить группу текущая группа "{group_name}"\n'
                             f''f'/group\n')


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
            keyboard_group.add(InlineKeyboardButton(
                text=f'{button[1]}', callback_data=f'{button[0]}')
            )
        keyboard_group.add(InlineKeyboardButton(text='Отмена', callback_data='start_admin'))
        name_state = callback.data
        chat_id = callback.message.chat.id

        data = await state.get_data()
        text = AdminTexts.get_menu_text(name_state)

        start_message = data.get('start_message')
        current_state = callback.data
        await state.set_state(AdminState.edit_group)
        await state.update_data(group_edit=current_state)
        try:
            await bot.edit_message_text(
                text=text, chat_id=chat_id, message_id=start_message, reply_markup=keyboard_group)

        except aiogram.utils.exceptions.MessageNotModified as err:
            logger.error(err)


@logger.catch
async def edit_group(callback: CallbackQuery, state: FSMContext) -> None:
    """Функция производит изменение id группы для получения списка пользователей с 'API'"""
    telegram_id = callback.from_user.id
    if str(telegram_id) in admins_list:
        data = await state.get_data()
        group_edit = data.get('group_edit')
        data['text'] = 'Группа не изменена'
        if group_edit == get_state_name(AdminState.waiting_group):
            GetcourseGroup.edit_club_group(callback.data)
            data['text'] = 'Изменена группа членов клуба '
        if group_edit == get_state_name(AdminState.club_group):
            GetcourseGroup.edit_waiting_group(callback.data)
            data['text'] = 'Изменена группа листа ожидания '

        data.pop('group_edit')
        callback.data = 'start_admin'
        await state.update_data(data)
        await state.set_state(AdminState.start_admin)
        await admin_menu_handler(callback, state)


@logger.catch
async def channel_registration(callback: CallbackQuery, state: FSMContext) -> None:
    """Функция для управления каналами и группами, которыми бот должен управлять"""

    telegram_id = callback.from_user.id
    if str(telegram_id) in admins_list:
        name_state = callback.data
        if name_state == 'stop_edit_channel':
            await state.set_state(AdminState.start_admin)
            callback.data = get_state_name(AdminState.start_admin)
            await admin_menu_handler(callback=callback, state=state)
            return
        if name_state == 'add_channel':
            await add_channel(callback=callback, state=state)
            return
        channels = Channel.get_channels()
        keyboard_group: 'InlineKeyboardMarkup' = InlineKeyboardMarkup()
        for channel in channels:
            keyboard_group.row(
                InlineKeyboardButton(text=f'{channel.name}', callback_data=f'{channel.channel_id}'),
                InlineKeyboardButton(text='удалить', callback_data='{channel.channel_id}')
            )
        keyboard_group.row(
            InlineKeyboardButton(text='Добавить', callback_data='add_channel'),
            InlineKeyboardButton(text='Закончить', callback_data='stop_edit_channel'))

        data = await state.get_data()
        chat_id = callback.message.chat.id
        text = AdminTexts.get_menu_text(name_state)

        additional_text = data.get('result', '')
        if additional_text:
            text = f'{additional_text}\n\n{text}'
            data.pop('result')
            await state.set_data(data)

        start_message = data.get('start_message')
        # current_state = callback.data
        # await state.set_state(AdminState.edit_group)
        # await state.update_data(group_edit=current_state)
        try:
            await bot.edit_message_text(
                text=text, chat_id=chat_id, message_id=start_message, reply_markup=keyboard_group)

        except aiogram.utils.exceptions.MessageNotModified as err:
            logger.error(err)


@logger.catch
async def add_channel(callback: CallbackQuery, state: FSMContext) -> None:
    """Функция запроса управления каналами канала которым бот должен управлять"""

    telegram_id = callback.from_user.id
    if str(telegram_id) in admins_list:
        data = await state.get_data()
        chat_id = callback.message.chat.id
        name_state = callback.data
        text = AdminTexts.get_menu_text(name_state)
        start_message = data.get('start_message')
        keyboard = AdminKeyboard.get_menu_keyboard(name_state)
        try:
            await bot.edit_message_text(
                text=text, chat_id=chat_id, message_id=start_message, reply_markup=keyboard)

        except aiogram.utils.exceptions.MessageNotModified as err:
            logger.error(err)


@logger.catch
async def edit_channel(message: Message, state: FSMContext) -> None:
    """Функция производит изменение id канала для управления"""
    data: str = message.text
    channel_id = 0
    try:
        channel_id = int('-100' + data)
    except ValueError as exc:
        logger.info(f'{exc.__traceback__.tb_frame}\n{exc}')
    callback = CallbackQuery()
    callback.message = message
    callback.from_user = message.from_user
    callback.data = get_state_name(AdminState.edit_channel_list)
    await message.delete()
    try:
        if not channel_id:
            data = '-100' + data.split('/')[-2]
            channel_id = int(data)
        channel: Chat = await bot.get_chat(channel_id)
        title = channel.title
        if not channel:
            raise ValueError('channel not found')
    except Exception as exc:
        logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')
        await state.update_data(result='Канал не найден попробуйте ещё раз')

        await channel_registration(callback=callback, state=state)
        return
    await state.update_data(result='Канал добавлен')
    Channel.add_channel(channel_id=channel_id, channel_name=title)
    await channel_registration(callback=callback, state=state)


@logger.catch
def admin_menu_register_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для функций данного модуля
    """
    # dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state="*")
    # dp.register_message_handler(
    #     cancel_handler, Text(startswith=["отмена", "cancel"], ignore_case=True), state="*")
    # dp.register_callback_query_handler(
    #     cancel_handler, Text(startswith=["отмена", "cancel"], ignore_case=True), state="*")
    #
    # dp.register_message_handler(admin_handler, commands=['админ', 'admin'], state="*")
    # dp.register_message_handler(
    #     admin_handler, Text(startswith=["админ", "admin"], ignore_case=True), state="*")

    dp.register_callback_query_handler(
        admin_handler, Text(startswith=["админ", "admin"], ignore_case=True), state="*")

    dp.register_callback_query_handler(
        admin_menu_handler,
        state=[AdminState.start_admin, AdminState.mailing_list, AdminState.exit]
    )

    # dp.register_message_handler(channel_registration, commands=["channel"])
    # dp.register_message_handler(edit_channel, state=AdminState.edit_channel_list)

    dp.register_callback_query_handler(
        group_registration, state=[AdminState.waiting_group, AdminState.club_group])
    dp.register_callback_query_handler(edit_group,  state=[AdminState.edit_group])

    dp.register_message_handler(edit_channel, state=[AdminState.edit_channel_list])
    dp.register_callback_query_handler(channel_registration, state=[AdminState.edit_channel_list])

    dp.register_message_handler(return_telegram_id_handler, commands=["myid"])
