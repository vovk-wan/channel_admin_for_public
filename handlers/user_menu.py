"""Модуль с основными обработчиками команд, сообщений и коллбэков"""

import datetime
from dataclasses import dataclass

import aiogram
import aiogram.utils.exceptions
from aiogram.dispatcher import FSMContext
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)
from aiogram.types.chat import ChatInviteLink

from config import logger, bot, EMOJI, LINK_EXPIRATION_TIME
from handlers import utils
from handlers.utils import get_all_admins, check_message_private
from keyboards import user
from models import User, Channel, Statuses
from scheduler_funcs import send_message_to_admin
from states import MenuState
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


@check_message_private
@logger.catch
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Ставит все состояния в нерабочие.
    Обработчик команды /cancel
    """
    await state.finish()
    await start_menu_handler(message, state=state)


@check_message_private
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
        try:
            await bot.delete_message(chat_id=chat_id, message_id=contact_message)
        except (
                aiogram.utils.exceptions.MessageCantBeDeleted,
                aiogram.utils.exceptions.MessageToDeleteNotFound,
        )as err:
            logger.error(err)
        data.pop('contact_message')
        await state.set_data(data)

    mailing = data.get('mailing')
    if mailing:
        data.pop('mailing')
        await state.set_data(data)

    start_message = data.get('start_message')
    if start_message:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=1)
        except (
                aiogram.utils.exceptions.MessageCantBeDeleted,
                aiogram.utils.exceptions.MessageToDeleteNotFound,
        ) as err:
            logger.error(err)
        data.pop('start_message')
        await state.set_data(data)

    try:
        start_message = await bot.send_message(
            chat_id=telegram_id, text=text, reply_markup=user.start_(telegram_id=telegram_id))
        await state.update_data(start_message=start_message.message_id)
    except (aiogram.utils.exceptions.MessageTextIsEmpty,
            aiogram.utils.exceptions.Unauthorized,
            aiogram.utils.exceptions.CantTalkWithBots,
            )as err:
        logger.error(err)
        logger.info(message.chat.type)
    if not mailing:
        try:
            await message.delete()
        except (
                aiogram.utils.exceptions.MessageCantBeDeleted,
                aiogram.utils.exceptions.MessageToDeleteNotFound,
        ) as err:
            logger.error(err)
            logger.info(message.chat.type)


@logger.catch
async def user_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """user menu"""
    name_state = callback.data

    data = await state.get_data()
    chat_id = callback.message.chat.id

    contact_message = data.get('contact_message')
    if contact_message:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=contact_message)
        except (
                aiogram.utils.exceptions.MessageCantBeDeleted,
                aiogram.utils.exceptions.MessageToDeleteNotFound,
        )as err:
            logger.error(err)
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
        menu = await bot.send_message(chat_id=callback.message.chat.id, text='menu')
        start_message = menu.message_id
        await state.update_data({'start_message': start_message})
        logger.debug('deleted start menu')
        # return

    if name_state == 'not_in_base':
        try:
            await bot.edit_message_text(
                text=' ☎️ ', chat_id=chat_id, message_id=start_message)
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
        keyboard: InlineKeyboardMarkup = (
            Keyboard.get_menu_keyboard('start')(telegram_id=telegram_id)
        )
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

    telegram_id = message.from_user.id
    phone = message.contact.phone_number
    contact_id = message.contact.user_id
    await message.delete()
    if contact_id != telegram_id:
        await message.answer('Данные не совпадают, ссылка выслана не будет')
        await start_menu_handler(message, state=state)
        return
    logger.info('Processing of invitation link requests begins :')

    user_data = User.add_challenger(telegram_id=telegram_id, phone=phone)
    new_state = 'start'
    if user_data:
        new_state = utils.get_position(user_data)
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
    user_data: User = User.get_users_by_telegram_id(telegram_id=telegram_id)
    if not user_data:
        await send_message_to_admin(f'ссылку запросил пользователь отсутствующий в базе\n'
                                    f'телеграм {telegram_id}')
        return 'https://google.com'

    if user_data.status not in [Statuses.entered, Statuses.returned, Statuses.privileged]:
        return 'Вас нет в списках членов клуба, ссылка выслана не будет.'
    if user_data.status not in [Statuses.entered, Statuses.returned, Statuses.privileged]:
        month = user_data.date_joining_club.month
        return f'Доступ откроется 1 - {month}'

    access = not user_data.got_invite
    answer = ''
    if not access:
        admins_name: tuple = await get_all_admins()
        answer = (f'Вы уже есть в базе данных обратитесь к администратору\n'
                  f'{EMOJI.hello}\n'
                  f'Администраторы:'
                  )
        answer += '\n' + '\n'.join(admins_name)
        return answer
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

    for channel in channels:
        try:
            await channel.unban(telegram_id)
            await channel.unban_sender_chat(telegram_id)
        except Exception as exc:
            logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')

        try:
            link: ChatInviteLink = await channel.create_invite_link(
                expire_date=expire_date,
                member_limit=1
            )
            answer += f'\n{channel.full_name}\n{link.invite_link}'
            User.got_invited(telegram_id=telegram_id)
        except Exception as err:
            logger.error(err)

    return answer
