"""Модуль с основными обработчиками команд, сообщений и коллбэков"""

import datetime
from dataclasses import dataclass

import aiogram
from aiogram.dispatcher.filters import Text
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.types.chat import ChatInviteLink

from aiogram.dispatcher import FSMContext
import aiogram.utils.exceptions
from config import logger, Dispatcher, bot, EMOJI, LINK_EXPIRATION_TIME, admins_list
from handlers.utils import get_user_position
from models import User, Channel, Statuses
from scheduler_funcs import send_message_to_admin
from states import MenuState, AdminState, get_state_name
from keyboards import user
from handlers import utils
# from handlers.admin_menu import admin_menu_handler
from texts.menu import TextsUser


@dataclass
class Keyboard:
    start: InlineKeyboardMarkup = user.start_
    about: InlineKeyboardMarkup = user.about_
    want: InlineKeyboardMarkup = user.want_
    reviews: InlineKeyboardMarkup = user.want_
    prices: InlineKeyboardMarkup = user.want_
    club_not_got_link: InlineKeyboardMarkup = user.link_
    club_got_link: InlineKeyboardMarkup = user.link_
    excluded: InlineKeyboardMarkup = user.excluded_
    wait_list: ReplyKeyboardMarkup = user.wait_list_
    challenger: ReplyKeyboardMarkup = user.challenger_
    not_in_base: ReplyKeyboardMarkup = user.not_in_base_
    get_invite_link: ReplyKeyboardMarkup = user.not_in_base_

    @classmethod
    def get_menu_keyboard(cls, name: str):
        try:
            return getattr(cls, name)
        except AttributeError as err:
            logger.info(f'{cls.__qualname__} exception: {err}')
            return cls.start


@logger.catch
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Ставит все состояния в нерабочие.
    Обработчик команды /cancel
    """
    await state.finish()
    await start_menu_handler(message, state=state)


@logger.catch
async def start_menu_handler(message: Message, state: FSMContext) -> None:
    """
        Функция - приветствие
        выводит основное меню и сообщение - основу под все кнопки
    """

    text = TextsUser.start()
    chat_id = message.chat.id
    telegram_id = message.from_user.id
    await state.set_state(MenuState.start)
    data = await state.get_data()
    contact_message = data.get('contact_message')
    if contact_message:
        await bot.delete_message(chat_id=chat_id, message_id=contact_message)
        data.pop('contact_message')
        await state.set_data(data)
    start_message = data.get('start_message')
    if not start_message:
        try:
            start_message = await bot.send_message(
                chat_id=telegram_id, text=text, reply_markup=user.start_(telegram_id=telegram_id))
        except aiogram.utils.exceptions.MessageTextIsEmpty as err:
            logger.error(err)
        await state.update_data(start_message=start_message.message_id)
        return
    try:
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=start_message,
            reply_markup=user.start_(telegram_id=telegram_id),
        )
    except (
                        aiogram.utils.exceptions.MessageNotModified,
                        aiogram.utils.exceptions.MessageTextIsEmpty
                ) as err:
        logger.error(err)
        await state.finish()
        await start_menu_handler(message=message, state=state)
        return
    await message.delete()

    # await bot.edit_message_reply_markup(
    #     reply_markup=user.start_(), chat_id=message.chat.id, message_id=start_message)


@logger.catch
async def user_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """user menu"""
    name_state = callback.data

    data = await state.get_data()
    chat_id = callback.message.chat.id

    contact_message = data.get('contact_message')
    if contact_message:
        await bot.delete_message(chat_id=chat_id, message_id=contact_message)
        data.pop('contact_message')
        await state.set_data(data)
    telegram_id = callback.from_user.id
    chat_id = callback.message.chat.id
    if name_state == 'want':
        name_state = utils.get_user_position(telegram_id)
    text = TextsUser.get_menu_text(name_state)()
    keyboard = Keyboard.get_menu_keyboard(name_state)(telegram_id=telegram_id)

    await state.set_state(MenuState.get_state_by_name(callback.data))
    start_message = data.get('start_message')
    if not start_message:
        logger.debug('deleted start menu')
        return

    if name_state == 'not_in_base':
        try:
            await bot.edit_message_text(
                text='контакт', chat_id=chat_id, message_id=start_message)
            contact_message = await bot.send_message(
                text=TextsUser.not_in_base(),
                chat_id=chat_id,
                reply_markup=keyboard
            )
            await state.update_data(contact_message=contact_message.message_id)
            return
        except (
                        aiogram.utils.exceptions.MessageNotModified,
                        aiogram.utils.exceptions.MessageTextIsEmpty
                ) as err:
            logger.error(err)
    elif name_state == 'get_invite_link':
        # channel_id = Channel.get_channel()
        await state.set_state(MenuState.start)
        answer = await get_link(telegram_id=telegram_id)

        text = f'{answer}\n{text}'
        try:
            await bot.edit_message_text(
                text=text, chat_id=chat_id, message_id=start_message)
        except (
                aiogram.utils.exceptions.MessageNotModified,
                aiogram.utils.exceptions.MessageTextIsEmpty
        ) as err:
            logger.error(err)

        text = TextsUser.get_menu_text('start')()
        keyboard: InlineKeyboardMarkup = Keyboard.get_menu_keyboard('start')(telegram_id=telegram_id)
        start_message = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
        await state.update_data({'start_message': start_message.message_id})
        return

        # text = TextsUser.get_menu_text('start')()
        # keyboard = Keyboard.get_menu_keyboard('start')(telegram_id=telegram_id)
        # await callback.answer()
    try:
        await bot.edit_message_text(
            text=text, chat_id=chat_id, message_id=start_message, reply_markup=keyboard)

    except (
                        aiogram.utils.exceptions.MessageNotModified,
                        aiogram.utils.exceptions.MessageTextIsEmpty
                ) as err:
        logger.error(err)

    except aiogram.utils.exceptions.ButtonURLInvalid as err:
        urls = [button.url for row in keyboard.inline_keyboard for button in row if button.url]
        logger.error(err)
        await send_message_to_admin(f'[Error]\n'
                                    f'неверные ссылки в DB {urls}')


@logger.catch
async def add_phone_number(message: Message, state: FSMContext):
    """Обработка запроса на получение ссылки и запись в базу"""
    # TODO декоратор на наличие канала
    # channel_id = Channel.get_channel()
    # if not channel_id:
    #     return
    telegram_id = message.from_user.id
    phone = message.contact.phone_number
    contact_id = message.contact.user_id
    await message.delete()
    if contact_id != telegram_id:
        await message.answer('Данные не совпадают, ссылка выслана не будет')
        await start_menu_handler(message, state=state)
        return
    logger.info('Processing of invitation link requests begins :')

    user = User.add_challenger(telegram_id=telegram_id, phone=phone)
    new_state = 'start'
    if user:
        new_state = utils.get_position(user)
    await state.set_state(MenuState.get_state_by_name(new_state))
    callback = CallbackQuery()
    callback.data = new_state
    callback.message = message
    callback.from_user = message.from_user
    await user_menu_handler(callback, state)


async def get_link(telegram_id: int) -> str:
    """function for make invite link"""
    # channel_id = Channel.get_channel()
    # if not channel_id:
    #     return
    user: User = User.get_users_by_telegram_id(telegram_id=telegram_id)
    if user.status not in [Statuses.entered, Statuses.returned]:
        return 'Вас нет в списках членов клуба, ссылка выслана не будет.'

    access = not user.got_invite
    answer = ''
    if not access:
        answer = (f'Вы уже есть в базе данных обратитесь к администратору\n'
                 f'{EMOJI.hello}\n'
                 f'Администраторы:')

    expire_date = datetime.datetime.now() + datetime.timedelta(hours=LINK_EXPIRATION_TIME)
    data = Channel.get_channels()
    if not data:
        return ('Не обнаружено доступных каналов.\n'
                'Попробуете сделать запрос позже.')

    channels = []
    for ch in data:
        try:
            result = await bot.get_chat(ch.channel_id)
            if result:
                channels.append(result)
        except Exception as err:
            logger.error(err)
    admins_name: set = set()
    for channel in channels:
        if access:
            try:
                await channel.unban(telegram_id)
                await channel.unban_sender_chat(telegram_id)
            except Exception as exc:
                logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')

        try:
            if access:
                link: ChatInviteLink = await channel.create_invite_link(
                    expire_date=expire_date,
                    member_limit=1
                )
                answer += f'\n{channel.full_name}\n{link.invite_link}'
                User.got_invited(telegram_id=telegram_id)
            else:
                admins = await channel.get_administrators()
                for admin in admins:
                    if not admin.user.is_bot:

                        admins_name.add(admin.user.mention)

        except Exception as err:
            logger.error(err)

    answer += '\n' + '\n'.join(admins_name)
    return answer
