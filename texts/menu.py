from dataclasses import dataclass

from config import logger, EMOJI


@dataclass
class TextsUser:
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

    # Текст если есть в листе ожидания
    wait_list: str = (
        'Текст если есть в листе ожидания'
    )

    # Текст сопровождение со ссылкой
    get_invite_link: str = (
        'Текст сопровождение с invite ссылкой'
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
class AdminTexts:
    """TODO Заменить на запросы к бд"""
    #  текст стартового меню администраторов
    start_admin: str = "hello admin"

    # изменение группы листа ожидания
    waiting_group: str = 'Текст изменение группы листа ожидания'

    # изменение группы для членов клуба
    club_group: str = 'Текст изменение группы членов клуба'

    # изменение каналов
    edit_channel_list: str = 'Текст изменение списка каналов'

    # изменение каналов
    add_channel: str = 'Текст добавить новый канал'

    # рассылка ссылок на оплату
    mailing_list: str = 'Текст изменение каналов'

    @classmethod
    @logger.catch
    def get_menu_text(cls, name: str):
        try:
            return getattr(cls, name)
        except AttributeError as err:
            logger.info(f'{cls.__qualname__} exception: {err}')
            return cls.start_admin
