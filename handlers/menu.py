import aiogram
import aiogram.utils.exceptions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import (Message, CallbackQuery)

from config import logger, Dispatcher, admins_list, bot
from handlers.admin_menu import (
    start_menu_admin, channel_registration, edit_channel,
    group_registration,
    return_telegram_id_handler, edit_group, mailing_list
)
from handlers.user_menu import (
    user_menu_handler, cancel_handler, add_phone_number, start_menu_handler
)
from handlers.utils import check_message_private
from states import MenuState, AdminState, get_state_name


@logger.catch
async def get_user_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MenuState.start)
    callback.message.from_user.id = callback.from_user.id
    if callback.data == 'get_user_menu':
        await state.update_data({'mailing': 'true'})
        await start_menu_handler(callback.message, state=state)
    else:
        callback.data = 'want'
        await state.set_state(MenuState.start)
        await state.update_data({'contact_message': callback.message.message_id})
        await user_menu_handler(callback, state)
    await callback.answer()


@logger.catch
async def get_invite_link_from_mailing(callback: CallbackQuery, state: FSMContext) -> None:
    """ function wrapper"""
    await state.set_state(MenuState.club_got_link)
    await state.update_data({'start_message': callback.message.message_id})
    callback.data = 'get_invite_link'
    await user_menu_handler(callback, state=state)
    try:
        await callback.answer()
    except Exception as err:
        logger.info(err)


@check_message_private
@logger.catch
async def command_admin_handler(message: Message, state: FSMContext) -> None:
    """
    Функция обработка команды админ
    """
    telegram_id = message.from_user.id
    if str(telegram_id) not in admins_list:
        return

    await state.set_state(AdminState.start_admin)
    await state.set_data({'start_message': message.message_id})
    callback = CallbackQuery()
    callback.from_user = message.from_user
    callback.message = message
    callback.data = get_state_name(AdminState.start_admin)
    await admin_menu_handler(callback, state)


@logger.catch
async def main_menu_handler(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Функция промежуточная
    """
    telegram_id = callback.from_user.id

    name_state = callback.data

    if name_state in ('about', 'admin') and str(telegram_id) in admins_list:
        await state.set_state(AdminState.start_admin)
        callback.data = get_state_name(AdminState.start_admin)
        await admin_menu_handler(callback=callback, state=state)
        return

    await user_menu_handler(callback=callback, state=state)


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
        count = await mailing_list()
        await bot.answer_callback_query(
            callback_query_id=callback.id, text=f'отправлено {count} сообщений')
        # await wait_text(callback, state)
        await state.set_state(AdminState.start_admin)
        callback.data = get_state_name(AdminState.start_admin)
        # await start_menu_admin(callback, state)
        try:
            await callback.answer()
        except aiogram.utils.exceptions.InvalidQueryID as err:
            logger.error(err)
        return
    else:
        await start_menu_admin(callback, state)
        try:
            await callback.answer()
        except aiogram.utils.exceptions.InvalidQueryID as err:
            logger.error(err)
        return


@logger.catch
def menu_register_handlers(dp: Dispatcher) -> None:
    """
    Регистратор для обработчиков
    """
    #  ********* функции user_menu
    dp.register_callback_query_handler(
        get_user_menu_handler,
        lambda callback: callback.data in ('get_user_menu', 'get_user_menu_want'),
        state='*'
    )

    dp.register_callback_query_handler(
        get_invite_link_from_mailing,
        lambda callback: callback.data == 'get_invite_link_from_mailing', state='*'
    )

    dp.register_message_handler(start_menu_handler, commands=["start"], state="*")
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
    dp.register_message_handler(return_telegram_id_handler, commands=["myid"])

    #  ********* функций admin_menu

    dp.register_message_handler(command_admin_handler, commands=["admin"], state="*")
    dp.register_callback_query_handler(
        admin_menu_handler,
        state=[AdminState.start_admin, AdminState.mailing_list, AdminState.exit]
    )

    dp.register_callback_query_handler(
        group_registration, state=[AdminState.waiting_group, AdminState.club_group])
    dp.register_callback_query_handler(edit_group, state=[AdminState.edit_group])

    dp.register_message_handler(edit_channel, state=[AdminState.edit_channel_list])
    dp.register_callback_query_handler(channel_registration, state=[AdminState.edit_channel_list])

    dp.register_message_handler(mailing_list, state=[AdminState.mailing_list])

    dp.register_message_handler(start_menu_handler)
