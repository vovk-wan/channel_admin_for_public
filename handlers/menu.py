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
from keyboards.admin import cancel
from handlers import utils

from handlers.admin_menu import (
    start_menu_admin, channel_registration, wait_text, edit_channel, group_registration,
    return_telegram_id_handler, edit_group, mailing_list
)
from handlers.user_menu import (
    user_menu_handler, cancel_handler, add_phone_number, start_menu_handler
)


@logger.catch
async def main_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция промежуточная
    """
    telegram_id = callback.from_user.id

    name_state = callback.data

    if name_state == 'about' and str(telegram_id) in admins_list:
        await state.set_state(AdminState.start_admin)
        callback.data = get_state_name(AdminState.start_admin)
        await admin_menu_handler(callback=callback, state=state)
        return
    # else:
    #     callback.data = get_state_name(AdminState.start_admin)
    # callback.data = new_state
    await user_menu_handler(callback=callback, state=state)
    # return


@logger.catch
async def admin_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция промежуточная
    """
    name_state = callback.data
    new_state = AdminState.get_state_by_name(name_state)
    await state.set_state(new_state)

    if name_state in [
        get_state_name(AdminState.waiting_group), get_state_name(AdminState.club_group)
    ]:
        await group_registration(callback, state)
        await callback.answer()
        return
    elif name_state == get_state_name(AdminState.edit_channel_list):
        await channel_registration(callback, state)
        await callback.answer()
        return
    elif name_state == get_state_name(AdminState.exit):
        await main_menu_handler(callback, state)
        await callback.answer()
        return
    elif name_state == get_state_name(AdminState.mailing_list):
        await wait_text(callback, state)
        await callback.answer()
        return
    else:
        await start_menu_admin(callback, state)
        await callback.answer()
        return


@ logger.catch
async def start_add_privileged(message: Message, state: FSMContext):
    """test manager"""
    telegram_id: str = str(message.from_user.id)
    user_is_superadmin: bool = telegram_id in admins_list
    if user_is_superadmin:
        await message.answer(
            "Перешлите (forward) мне любое сообщение пользователя, "
            "которого вы хотите сделать привилегированным.",
            reply_markup=cancel()
        )
        await AdminState.add_privileged.set()
    else:
        logger.info(f"User {telegram_id} try to add user.")


@logger.catch
async def check_new_user_is_exists_handler(message: Message, state: FSMContext) -> None:
    """Получает сообщение от админа и добавляет пользователя в БД

    """
    logger.debug(f"Add user message: {message}")
    if not message.forward_from:
        await message.answer(
            "Нужно переслать (forward) любое сообщение из телеграма от пользователя, "
            "которого вы хотите добавить. Если не получается - скажите пользователю, "
            "чтоб разрешил пересылку сообшений в своих настройках телеграма.",
            reply_markup=cancel()
        )
        return
    text = 'Не удалось сделать пользователя привилегированным'
    new_user_telegram_id: str = message.forward_from.id
    new_user_nickname: str = message.forward_from.username
    if User.add_privileged_status_by_telegram_id(message.forward_from.id):
        text = 'Пользователь стал привилегированным'

    await message.answer(
        f"{text} {new_user_telegram_id}: {new_user_nickname}",
        reply_markup=cancel()
    )

@ logger.catch
async def start_add_privileged(message: Message, state: FSMContext):
    """test manager"""
    telegram_id: str = str(message.from_user.id)
    user_is_superadmin: bool = telegram_id in admins_list
    if user_is_superadmin:
        await message.answer(
            "Перешлите (forward) мне любое сообщение пользователя, "
            "которого вы хотите сделать привилегированным.",
            reply_markup=cancel()
        )
        await AdminState.add_privileged.set()
    else:
        logger.info(f"User {telegram_id} try to add user.")


@logger.catch
async def check_new_user_is_exists_handler(message: Message, state: FSMContext) -> None:
    """Получает сообщение от админа и добавляет пользователя в БД

    """
    logger.debug(f"Add user message: {message}")
    if not message.forward_from:
        await message.answer(
            "Нужно переслать (forward) любое сообщение из телеграма от пользователя, "
            "которого вы хотите добавить. Если не получается - скажите пользователю, "
            "чтоб разрешил пересылку сообшений в своих настройках телеграма.",
            reply_markup=cancel()
        )
        return
    text = 'Не удалось снять статус  пользователя "привилегированный"'
    user_telegram_id: str = message.forward_from.id
    user_nickname: str = message.forward_from.username
    if User.delete_privileged_status_by_telegram_id(user_telegram_id):
        text = 'У пользователя снят статус "привилегированный"'

    await message.answer(
        f"{text} {user_telegram_id}: {user_nickname}",
        reply_markup=cancel()
    )


@logger.catch
def menu_register_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для обработчиков
    """
    #  ********* функции user_menu
    dp.register_message_handler(start_menu_handler, commands=["start"], state="*")
    dp.register_message_handler(start_add_privileged, commands=["privileged"], state="*")
    dp.register_message_handler(start_add_privileged, state=[AdminState.add_privileged])
    dp.register_message_handler(start_add_privileged, state=[AdminState.delete_privileged])
    dp.register_message_handler(
        start_menu_handler, Text(startswith=["назад"], ignore_case=True), state="*")
    dp.register_callback_query_handler(main_menu_handler, state=[
        MenuState.start, MenuState.about, MenuState.challenger, MenuState.excluded,
        MenuState.club_got_link, MenuState.club_not_got_link, MenuState.want,
        MenuState.reviews, MenuState.prices, MenuState.not_in_base, MenuState.wait_list
    ])
    dp.register_message_handler(cancel_handler, commands=['отмена', 'cancel'], state="*")
    dp.register_message_handler(
        add_phone_number, content_types=['contact'], state=MenuState.want)

    #  ********* функций admin_menu

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

    dp.register_message_handler(mailing_list, state=[AdminState.mailing_list])
