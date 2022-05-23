"""Модуль с основными обработчиками команд, сообщений и коллбэков"""

import datetime
from dataclasses import dataclass

import aiogram
from aiogram.dispatcher.filters import Text
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup, ReplyKeyboardMarkup)
from aiogram.types.chat import ChatInviteLink

from aiogram.dispatcher import FSMContext
import aiogram.utils.exceptions
from config import logger, Dispatcher, bot, EMOJI, LINK_EXPIRATION_TIME, admins_list
from models import User, Channel
from states import MenuState, AdminState, get_state_name
from keyboards import user_menu
from handlers import utils
from handlers.admin_menu import admin_menu_handler


@dataclass
class Texts:
    """TODO Заменить на запросы к бд"""
    #  Приветственное сообщение Основное меню
    start: str = (
        f"Здравствуйте! {EMOJI.hello}\n"
        f"\n"
        f"Я бот Закрытого финансового клуба Effective Finance.\n"
        f"\n"
        f"Для того, чтобы получить пригласительную ссылку "
        f"в основную группу Клуба, наберите команду"
        f" /invite и следуйте дальнейшим инструкциям."
    )

    # Текст о клубе
    about: str = 'Текст о клубе'

    # Текст Прайс
    prices: str = 'Текст Прайс'

    # Отзывы
    reviews: str = 'Отзывы'

    # Текст после хочу в клуб если нет в базе телеграм ид
    not_in_base: str = (
        'Текст после хочу в клуб если нет в базе телеграм ид'
    )

    # Текст после хочу в клуб если не оплатил и первый раз в клубе, но нет в листе ожидания
    challenger: str = (
        'Текст после хочу в клуб если не оплатил и первый раз в клубе, но нет в листе ожидания'
    )

    # Текст после хочу в клуб если оплатил в клубе и не получал ссылку
    club_not_got_link: str = 'Текст после хочу в клуб если оплатил в клубе и не получал ссылку'

    # Текст после хочу в клуб уже оплатил уже в клубе но получал ссылку
    club_got_link: str = (
        'Текст после хочу в клуб уже оплатил уже в клубе но получал ссылку'
    )

    # Текст после хочу в клуб если не оплатил, но был уже в клубе
    excluded: str = (
        'Текст после хочу в клуб если не оплатил но уже был в клубе'
    )

    # Текст если есть в листе ожидания  TODO В группе лист ожидания?
    wait_list: str = (
        'Текст если есть в листе ожидания'
    )

    # Текст меню администратора
    admin_menu: str = (
        'Текст меню администратора'
    )

    @classmethod
    @logger.catch
    def get_menu_text(cls, name: str):
        try:
            return getattr(cls, name)
        except AttributeError as err:
            logger.info(f'{cls.__qualname__} exception: {err}')
            return cls.start


@dataclass
class Keyboard:
    start: InlineKeyboardMarkup = user_menu.start_()
    about: InlineKeyboardMarkup = user_menu.about_()
    want: InlineKeyboardMarkup = user_menu.want_()
    reviews: InlineKeyboardMarkup = user_menu.want_()
    prices: InlineKeyboardMarkup = user_menu.want_()
    club_not_got_link: InlineKeyboardMarkup = user_menu.link_()
    club_got_link: InlineKeyboardMarkup = InlineKeyboardMarkup(row_width=1).add(
                                                                user_menu.inline_button_start())
    excluded: InlineKeyboardMarkup = user_menu.excluded_()
    wait_list: ReplyKeyboardMarkup = InlineKeyboardMarkup(row_width=1).add(
                                                                user_menu.inline_button_start())
    challenger: ReplyKeyboardMarkup = user_menu.challenger_()
    not_in_base: ReplyKeyboardMarkup = user_menu.not_in_base_()

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
    await start_handler(message, state=state)


@logger.catch
async def start_handler(message: Message, state: FSMContext) -> None:
    """
        Функция - приветствие
        выводит основное меню и сообщение - основу под все кнопки
    """
    text = Texts.start
    chat_id = message.chat.id
    await state.set_state(MenuState.start)
    await message.delete()
    data = await state.get_data()
    contact_message = data.get('contact_message')
    if contact_message:
        await bot.delete_message(chat_id=chat_id, message_id=contact_message)
        data.pop('contact_message')
        await state.set_data(data)
    start_message = data.get('start_message')
    if not start_message:
        start_message = await message.answer(text=text, reply_markup=user_menu.start_())
        await state.update_data(start_message=start_message.message_id)
        return
    try:
        await bot.edit_message_text(
            text=text,
            chat_id=message.chat.id,
            message_id=start_message,
            reply_markup=user_menu.start_(),
        )
    except aiogram.utils.exceptions.MessageNotModified as err:
        logger.error(err)

    # await bot.edit_message_reply_markup(
    #     reply_markup=user_menu.start_(), chat_id=message.chat.id, message_id=start_message)


@logger.catch
async def menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция промежуточная
    """
    telegram_id = callback.from_user.id
    chat_id = callback.message.chat.id
    data = await state.get_data()

    contact_message = data.get('contact_message')
    if contact_message:
        await bot.delete_message(chat_id=chat_id, message_id=contact_message)
        data.pop('contact_message')
        await state.set_data(data)

    name_state = callback.data

    if name_state == 'want':
        name_state = utils.get_user_position(telegram_id)

    if name_state == 'about' and str(telegram_id) in admins_list:
        await state.set_state(AdminState.start_admin)
        callback.data = get_state_name(AdminState.start_admin)
        await admin_menu_handler(callback=callback, state=state)
        return

    text = Texts.get_menu_text(name_state)
    keyboard = Keyboard.get_menu_keyboard(name_state)

    await state.set_state(MenuState.get_state(callback.data))

    start_message = data.get('start_message')
    if not start_message:
        # TODO заполнить проверить все варианты
        logger.debug('menu_handler')
        return
    if name_state == 'not_in_base':
        await bot.edit_message_text(
            text='контакт', chat_id=chat_id, message_id=start_message)
        contact_message = await bot.send_message(
            chat_id=chat_id,
            text='Нажмите пожалуйста на кнопку отправить контакт',
            reply_markup=keyboard
        )
        await state.update_data(contact_message=contact_message.message_id)
        return
    elif name_state == 'get_invite_link':
        channel_id = Channel.get_channel()
        link = await get_link(telegram_id=telegram_id, channel_id=channel_id)
        text = f'{text} \n{link}'
        await bot.edit_message_text(text=text, chat_id=chat_id, message_id=start_message)

        text = Texts.get_menu_text('start')
        keyboard = Keyboard.get_menu_keyboard('start')
        start_message = await bot.send_message(chat_id=chat_id, text=text, reply_markup=keyboard)
        await state.update_data(contact_message=start_message.message_id)
        return
    try:
        await bot.edit_message_text(
            text=text, chat_id=chat_id, message_id=start_message, reply_markup=keyboard)

    except aiogram.utils.exceptions.MessageNotModified as err:
        logger.error(err)


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
        await start_handler(message, state=state)
        return
    logger.info('Processing of invitation link requests begins :')

    # TODO добавить пользователя
    user = User.add_challenger(telegram_id=telegram_id, phone=phone)
    new_state = 'start'
    if user:
        new_state = utils.get_position(user)
    await state.set_state(MenuState.get_state(new_state))
    callback = CallbackQuery()
    callback.data = new_state
    callback.message = message
    callback.from_user = message.from_user
    await menu_handler(callback, state)


async def get_link(telegram_id: int, channel_id):
    expire_date = datetime.datetime.now() + datetime.timedelta(hours=LINK_EXPIRATION_TIME)
    try:
        await bot.unban_chat_member(channel_id, telegram_id)
    except Exception as exc:
        logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')
    try:
        link: ChatInviteLink = await bot.create_chat_invite_link(
            channel_id, expire_date.timestamp(), 1)
        # await message.answer(
        #     text=link.invite_link)
        # await message.answer(
        #     f'Ссылка действительна в течении {LINK_EXPIRATION_TIME} часов',
        #     reply_markup=ReplyKeyboardRemove())
        return link.invite_link
    except Exception as exc:
        logger.error(f'{exc.__traceback__.tb_frame}\n{exc}')


@logger.catch
def user_menu_register_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для функций данного модуля
    """
    dp.register_message_handler(start_handler, commands=["start"], state="*")
    dp.register_message_handler(
        start_handler, Text(startswith=["назад"], ignore_case=True), state="*")
    dp.register_callback_query_handler(menu_handler, state=[
        MenuState.start, MenuState.about, MenuState.challenger, MenuState.excluded,
        MenuState.club_got_link, MenuState.club_not_got_link, MenuState.want,
        MenuState.reviews, MenuState.prices, MenuState.not_in_base, MenuState.wait_list
    ])
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state="*")
    dp.register_message_handler(
        add_phone_number, content_types=['contact'], state=MenuState.want)
