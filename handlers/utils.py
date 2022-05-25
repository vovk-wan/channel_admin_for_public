from models import User, Statuses


def get_position(user: User) -> str:
    result = 'challenger'

    if user.status == Statuses.challenger:
        result = 'challenger'
    elif user.status in (Statuses.entered, Statuses.returned, Statuses.privileged) and user.got_invite:
        result = 'club_got_link'
    elif user.status in (Statuses.entered, Statuses.returned, Statuses.privileged) and not user.got_invite:
        result = 'club_not_got_link'
    elif user.status == Statuses.excluded:
        result = 'excluded'
    elif user.status == Statuses.waiting:
        result = 'wait_list'

    return result


def get_user_position(telegram_id: int) -> str:
    """
    TODO запросить в каком списке находится пользователь вернуть строкой позицию
    TODO кажется лишняя
    примерный выбор
        club_not_got_link: в клубе ссылку не получал
        club_got_link: в клубе ссылку получал
        excluded: исключен
        wait_list:  не в клубе зарегистрирован не оплачено
        challenger: в клубе не был в списке нет
        'not_in_base': нет в базе
    """
    user = User.get_users_by_telegram_id(telegram_id=telegram_id)
    if user:
        return get_position(user)

    return 'not_in_base'



