"""Модуль с основными обработчиками команд, сообщений и коллбэков"""

import datetime
from dataclasses import dataclass

import aiogram
from aiogram.dispatcher.filters import Text
from aiogram.types import (Message, CallbackQuery, InlineKeyboardMarkup,
                           InlineKeyboardButton, ReplyKeyboardRemove,
                           ReplyKeyboardMarkup, KeyboardButton)
from aiogram.types.chat import ChatInviteLink, Chat

from aiogram.dispatcher import FSMContext

from keyboard import cancel_keyboard
from config import logger, Dispatcher, bot, EMOJI, admins_list, LINK_EXPIRATION_TIME
from models import User, Group, Channel
from states import UserState, AdminState, MenyState
from keyboards import user_menu
from handlers import utils


@dataclass
class Texts:
    """TODO Заменить на запросы к бд"""
    #  Приветственное сообщение Основное меню
    start: str = (f"Здравствуйте! {EMOJI.hello}\n"
            f"\n"
            f"Я бот Закрытого финансового клуба Effective Finance.\n"
            f"\n"
            f"Для того, чтобы получить пригласительную ссылку "
             f"в основную группу Клуба, наберите команду"
            f" /invite и следуйте дальнейшим инструкциям.")

    # Текст о клубе
    about: str = 'Text about club'

    # Прайс
    prices: str = 'prices'

    # Отзывы
    reviews: str = 'reviewers'

    # Текст после хочу в клуб если не оплатил и первый раз в клубе или нет в базе телеграм ид
    challenger: str = (
        'Text when a person is in the club for the first time and is already on the waiting list, '
        'but the course has not been paid'
    )


    # Текст после хочу в клуб если оплатил в клубе и не получал ссылку
    club_not_got_link: str = 'Text when the person was already in the club and the course was paid'

    # Текст после хочу в клуб уже оплатил уже в клубе но получал ссылку
    club_got_link: str = (
        'Text when the person was already in the club and the course was paid'
    )

    # Текст после хочу в клуб если не оплатил но уже в клубе
    club_not_paid: str = (
        'Text when a person has already been in the club and is already on the waiting list, '
        'but the course has not been paid'
    )

    # Текст после отправки заявки в клуб  TODO В группе лист ожидания?
    wait_list: str = (
        'Text when the person applied to join the club'
    )

    # Текст меню администратора
    admin_menu: str = (
        'Text when the person applied to join the club'
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
    club_not_paid: InlineKeyboardMarkup = user_menu.club_not_paid_()
    wait_list: ReplyKeyboardMarkup = InlineKeyboardMarkup(row_width=1).add(
                                                                user_menu.inline_button_start())
    challenger: ReplyKeyboardMarkup = user_menu.challenger_()

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
    await state.set_state(MenyState.start)
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

    text = Texts.get_menu_text(name_state)
    keyboard = Keyboard.get_menu_keyboard(name_state)

    await state.set_state(MenyState.get_state(callback.data))

    start_message = data.get('start_message')
    if not start_message:
        # TODO заполнить проверить все варианты
        pass
        return
    if name_state == 'challenger':

        await bot.edit_message_text(
            text='контакт', chat_id=chat_id, message_id=start_message)
        contact_message = await bot.send_message(
            chat_id=chat_id,
            text='Нажмите пожалуйста на кнопку отправить контакт',
            reply_markup=keyboard
        )
        await state.update_data(contact_message=contact_message.message_id)
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

    # **** add user *****
    # TODO добавить пользователя

    # user = User.get_user_by_phone(phone[-10:])
    # user.telegram_id = telegram_id
    # user.save()
    pass
    # **** end add user *****

    new_state = utils.get_user_position(telegram_id)
    if new_state == 'challenger':
        new_state = 'start'
        # TODO заглушка циркуляции
    await state.set_state(MenyState.get_state(new_state))
    callback = CallbackQuery()
    callback.data = new_state
    callback.message = message
    callback.from_user = message.from_user
    await menu_handler(callback, state)
        # await message.answer(
        #     f'{EMOJI.sad} Извините, пользователь с таким телефоном в базе не найден.\n'
        #     f'Возможно база данных ещё не обновилась', reply_markup=ReplyKeyboardRemove())
        # return


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
def menu_register_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для функций данного модуля
    """
    dp.register_message_handler(start_handler, commands=["start"], state="*")
    dp.register_message_handler(
        start_handler, Text(startswith=["назад"], ignore_case=True), state="*")
    dp.register_callback_query_handler(menu_handler, state=[
        MenyState.start, MenyState.about, MenyState.challenger, MenyState.club_not_paid,
        MenyState.club_got_link, MenyState.club_not_got_link, MenyState.want,
        MenyState.reviews, MenyState.prices
    ])
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state="*")
    dp.register_message_handler(
        add_phone_number, content_types=['contact'], state=MenyState.want)
