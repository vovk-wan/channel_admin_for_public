"""Модуль с основными обработчиками команд, сообщений и нажатие inline кнопок"""

import datetime

from aiogram.types import (Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton)
from aiogram.types.chat import ChatInviteLink, Chat

from aiogram.dispatcher import FSMContext

from config import logger, Dispatcher, bot, EMOJI, LINK_EXPIRATION_TIME
from models import User, Channel
from states import UserState


@logger.catch
async def invitation_link_request(message: Message):
    """Функция для запроса invite ссылки на канал"""
    channel_id = Channel.get_channel()
    if not channel_id:
        return
    user_id = message.from_user.id

    channel: Chat = await bot.get_chat(channel_id)
    await channel.get_member(message.from_user.id)
    # member = await channel.get_member(message.from_user.id)
    # # if member.status == 'member':
    # link = channel.invite_link
    user = User.get_users_by_telegram_id(user_id)

    if user:
        admins_name = ''
        if channel:
            admins = await channel.get_administrators()
            for admin in admins:
                if not admin.user.is_bot:
                    admins_name += admin.user.mention + '\n'
            await message.answer(f'Вы уже есть в базе данных обратитесь к администратору\n'
                                 f'{EMOJI.hello}\n'
                                 f'Администраторы:\n'
                                 f'{admins_name}')
        return

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(KeyboardButton(text='Отправить контакт', request_contact=True,))

    await UserState.wait_telephone_number.set()
    await message.answer(
        f'{EMOJI.hello}  Нажмите пожалуйста на кнопку "Отправить контакт"',
        reply_markup=keyboard
    )


@logger.catch
async def add_phone_number(message: Message, state: FSMContext):
    """Обработка запроса на получение ссылки и запись в базу"""
    channel_id = Channel.get_channel()
    if not channel_id:
        return
    user_id = message.from_user.id
    phone = message.contact.phone_number
    contact_id = message.contact.user_id
    if contact_id != user_id:
        await message.answer('Данные не совпадают, ссылка выслана не будет')
        return
    logger.info('Processing of invitation link requests begins :')
    user = User.get_user_by_phone(phone[-10:])
    if not user:
        await message.answer(
            f'{EMOJI.sad} Извините, пользователь с таким телефоном в базе не найден.\n'
            f'Возможно база данных ещё не обновилась', reply_markup=ReplyKeyboardRemove())
        return
    expire_date = datetime.datetime.now() + datetime.timedelta(hours=LINK_EXPIRATION_TIME)
    try:
        await bot.unban_chat_member(channel_id, user_id)
    except Exception as exc:
        logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')
    try:
        link: ChatInviteLink = await bot.create_chat_invite_link(
            channel_id, expire_date.timestamp(), 1)
        await message.answer(
            text=link.invite_link)
        await message.answer(
            f'Ссылка действительна в течении {LINK_EXPIRATION_TIME} часов',
            reply_markup=ReplyKeyboardRemove())
        user.telegram_id = user_id
        user.save()
    except Exception as exc:
        logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')
    await message.delete()
    await state.finish()


@logger.catch
async def message_handler(message: Message) -> None:
    """Функция - приветствие"""
    await message.answer(
        f"Здравствуйте! {EMOJI.hello}\n"
        f"\n"
        f"Я бот Закрытого финансового клуба Effective Finance.\n"
        f"\n"
        f"Для того, чтобы получить пригласительную ссылку в основную группу Клуба, наберите команду"
        f" /invite и следуйте дальнейшим инструкциям."
        )


@logger.catch
def register_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для функций данного модуля
    """
    dp.register_message_handler(invitation_link_request, commands=["invite"])
    # dp.register_message_handler(
    #     add_phone_number, content_types=['contact'], state=UserState.wait_telephone_number)
