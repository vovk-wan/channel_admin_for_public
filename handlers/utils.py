
def get_position(telegram_id: str) -> list:
    pos = 40
    if pos == 1:
        return ['club', 'got_link']
    elif pos == 2:
        return ['club', 'not_got_link']
    elif pos == 3:
        return ['club', 'not_paid']
    elif pos == 4:
        return ['wait_list']
    else:
        return ['challenger']


def get_user_position(telegram_id: str) -> str:
    """
    TODO запросить в каком списке находится пользователь вернуть строкой позицию
    примерный выбор
        club_not_got_link: в клубе ссылку не получал
        club_got_link: в клубе ссылку получал
        club_not_paid: в клубе ссылку получал
        wait_list:  не в клубе зарегистрирован не оплачено
        challenger: в клубе не был в списке нет
    """
    position: list = get_position(telegram_id)
    return '_'.join(position)


