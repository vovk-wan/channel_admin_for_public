"""Модуль с основными обработчиками команд, сообщений и нажатия inline кнопок"""

from aiogram.dispatcher.filters import Text
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton, ReplyKeyboardRemove)
from aiogram.types.chat import Chat

from aiogram.dispatcher import FSMContext

from keyboards.admin import cancel_keyboard
from config import logger, Dispatcher, bot, EMOJI, admins_list
from models import Group, Channel
from states import AdminState


@logger.catch
async def admin_handler(message: Message, state: FSMContext) -> None:
    await state.finish()
    user_id = message.from_user.id
    if str(user_id) in admins_list:
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
async def group_registration(message: Message) -> None:
    """Функция запроса изменения группы для получения списка пользователей с 'API'"""
    user_id = message.from_user.id
    if str(user_id) in admins_list:
        groups = Group.get_all_group_channel()
        keyboard_group: 'InlineKeyboardMarkup' = InlineKeyboardMarkup(row_width=1)
        for button in groups:
            keyboard_group.add(InlineKeyboardButton(
                text=f'{button[1]}', callback_data=f'{button[0]}')
            )

        await message.answer(
            'Группы',
            reply_markup=keyboard_group
        )
        await message.answer(
            'Выберите группу',
            reply_markup=cancel_keyboard()
        )

        await AdminState.group_registration.set()


@logger.catch
async def edit_group(callback: CallbackQuery, state: FSMContext) -> None:
    """Функция производит изменение id группы для получения списка пользователей с 'API'"""
    user_id = callback.from_user.id
    if str(user_id) in admins_list:
        Channel.edit_group(int(callback.data))
        await callback.answer()
        await callback.message.delete()
        await callback.message.answer(
            f'выбрана группа {callback.data}', reply_markup=ReplyKeyboardRemove())
    await state.finish()


@logger.catch
async def channel_registration(message: Message) -> None:
    """Функция запроса изменения канала которым бот должен управлять"""

    user_id = message.from_user.id
    if str(user_id) in admins_list:
        await AdminState.channel_registration.set()
        await message.answer(
            'Введите id канала, или ссылку на любое сообщение в канале',
            reply_markup=cancel_keyboard()
        )


@logger.catch
async def edit_channel(message: Message, state: FSMContext) -> None:
    """Функция производит изменение id канала для управления"""

    data: str = message.text
    channel_id = 0
    try:
        channel_id = int('-100' + data)
    except ValueError as exc:
        logger.info(f'{exc.__traceback__.tb_frame}\n{exc}')

    try:
        if not channel_id:
            data = '-100' + data.split('/')[-2]
            channel_id = int(data)
        channel = await bot.get_chat(channel_id)

        if not channel:
            raise ValueError('channel not found')
    except Exception as exc:
        logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')

        await message.answer(f'{EMOJI.sad} Канал не найден попробуйте ещё раз')
        return
    Channel.edit_channel(channel_id)
    await message.answer(f'{EMOJI.like} Канал изменен')
    await state.finish()


@logger.catch
def admin_menu_register_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для функций данного модуля
    """
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state="*")
    dp.register_message_handler(
        cancel_handler, Text(startswith=["отмена", "cancel"], ignore_case=True), state="*")
    dp.register_callback_query_handler(
        cancel_handler, Text(startswith=["отмена", "cancel"], ignore_case=True), state="*")

    dp.register_message_handler(admin_handler, commands=['админ', 'admin'], state="*")
    dp.register_message_handler(
        admin_handler, Text(startswith=["админ", "admin"], ignore_case=True), state="*")
    dp.register_callback_query_handler(
        admin_handler, Text(startswith=["админ", "admin"], ignore_case=True), state="*")

    dp.register_message_handler(channel_registration, commands=["channel"])
    dp.register_message_handler(edit_channel, state=AdminState.channel_registration)

    dp.register_message_handler(group_registration, commands=["group"])
    dp.register_callback_query_handler(edit_group, state=AdminState.group_registration)

    dp.register_message_handler(return_telegram_id_handler, commands=["myid"])
