import datetime
from dataclasses import dataclass
import os
from typing import Any, List, Tuple

from peewee import (
    CharField, BooleanField, IntegerField, TextField, DateTimeField, BigIntegerField)
from peewee import Model

from config import logger, db


@dataclass(frozen=True)
class SourceData:
    waiting_list: str = 'waiting_list'
    club: str = 'club'


@dataclass(frozen=True)
class Statuses:
    challenger: str = 'challenger'
    waiting: str = 'waiting'
    entered: str = 'entered'
    returned: str = 'returned'
    excluded: str = 'excluded'
    privileged: str = 'privileged'


@dataclass(frozen=True)
class DefaultTexts:
    start: str = 'Тест в основном меню'
    about: str = 'Текст о клубе'
    prices: str = 'Текст о тарифах'
    reviews: str = 'Текст с отзывами'
    for_mailing: str = 'Текст со ссылкой на оплату'
    for_invite: str = 'Текст вместе с пригласительными ссылками'
    for_get_phone: str = 'Текст для запроса контакта'
    for_challenger: str = '"Хочу в клуб" новичков'
    for_waiting_list: str = '"Хочу в клуб" для листа ожидания'
    for_excluded: str = '"Хочу в клуб" исключенных'
    for_entered: str = '"Хочу в клуб" для тех кто может получить ссылку'
    for_entered_got_link: str = '"Хочу в клуб" для тех кто получал ссылку'

    link_waiting_list: str = 'https://getcourse.io/'
    link_to_pay: str = 'https://getcourse.io/'


class BaseModel(Model):
    """A base model that will use our Sqlite database."""

    class Meta:
        database = db
        order_by = 'date_at'


class Text(BaseModel):
    """Class for text message table"""
    start = TextField(verbose_name='Текст в основном меню')
    about = TextField(verbose_name='Текст о клубе')
    prices = TextField(verbose_name='Текст с ценами')
    reviews = TextField(verbose_name='Текст с отзывами')
    for_mailing = TextField(verbose_name='Текст в рассылки на оплату')
    for_invite = TextField(verbose_name='Текст вместе с инвайт ссылками')
    for_get_phone = TextField(verbose_name='Текст с запросом контакта')
    for_challenger = TextField(verbose_name='"Хочу в клуб" новичков')
    for_waiting_list = TextField(verbose_name='"Хочу в клуб" для листа ожидания')
    for_excluded = TextField(verbose_name='"Хочу в клуб" исключенных')
    for_entered = TextField(verbose_name='"Хочу в клуб" для тех кто может получить ссылку')
    for_entered_got_link = TextField(verbose_name='"Хочу в клуб" для тех кто уже получал ссылку')

    link_waiting_list = CharField(max_length=255, verbose_name='Ссылка на лист ожидания')
    link_to_pay = CharField(verbose_name='Ссылка на лист ожидания')
    # link_to_pay_excluded = CharField(verbose_name='Ссылка на оплату для исключенных')
    # link_to_pay_waiting_list = CharField(
    #     verbose_name='Ссылка на оплату пользователям в листе ожидания')

    class Meta:
        db_table = "text_messages"

    @classmethod
    @logger.catch
    def get_start_text(cls):
        """Возвращает текст в основном меню"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.start if data.start else 'no text'

    @classmethod
    @logger.catch
    def get_about_text(cls):
        """Возвращает Текст о клубе"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.about

    @classmethod
    @logger.catch
    def get_prices_text(cls):
        """Возвращает Текст с ценами"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.prices

    @classmethod
    @logger.catch
    def get_reviews_text(cls):
        """Возвращает Текст с отзывами"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.reviews

    @classmethod
    @logger.catch
    def get_for_mailing_text(cls):
        """Возвращает Текст в рассылки на оплату"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.for_mailing

    @classmethod
    @logger.catch
    def get_for_invite_text(cls):
        """Возвращает Текст вместе с инвайт ссылками"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.for_invite

    @classmethod
    @logger.catch
    def get_want_for_get_phone_text(cls):
        """Возвращает Текст с запросом контакта"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.for_get_phone

    @classmethod
    @logger.catch
    def get_want_for_challenger_text(cls):
        """Возвращает "Хочу в клуб" новичков"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.for_challenger

    @classmethod
    @logger.catch
    def get_want_for_waiting_list_text(cls):
        """Возвращает "Хочу в клуб" для листа ожидания"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.for_waiting_list

    @classmethod
    @logger.catch
    def get_want_for_excluded_text(cls):
        """Возвращает "Хочу в клуб" исключенных"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.for_excluded

    @classmethod
    @logger.catch
    def get_want_for_entered_text(cls):
        """Возвращает "Хочу в клуб" для тех кто может получить ссылку"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.for_entered

    @classmethod
    @logger.catch
    def get_want_for_entered_got_link_text(cls):
        """Возвращает "Хочу в клуб" для тех кто уже получал ссылку"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.for_entered_got_link

    @classmethod
    @logger.catch
    def get_link_waiting_list_text(cls):
        """Возвращает ссылку в лист ожидания"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.link_waiting_list

    @classmethod
    @logger.catch
    def get_link_to_pay(cls):
        """Возвращает ссылку на оплату"""
        data = cls.select().first()
        if not data:
            data = DefaultTexts
        return data.link_to_pay

    # @classmethod
    # @logger.catch
    # def get_link_paid_excluded(cls):
    #     """Возвращает ссылку на оплату для тех кто был в клубе"""
    #     data = cls.select().first()
    #     if not data:
    #         data = DefaultTexts
    #     return data.link_paid_excluded

    # @classmethod
    # @logger.catch
    # def get_link_paid_waiting_list(cls):
    #     """Возвращает ссылку на оплату для листа ожидания"""
    #     data = cls.select().first()
    #     if not data:
    #         data = DefaultTexts
    #     return data.link_paid_waiting_list


class MessageNewStatus(BaseModel):
    """Class for text message  table"""
    waiting = TextField(verbose_name='Текст после регистрации в листе ожидания')
    entered = TextField(verbose_name='Текст после вступления в клуб')
    returned = TextField(verbose_name='Текст после возвращения в клуб')
    excluded = TextField(verbose_name='Текст после исключения из клуба')
    privileged = TextField(verbose_name='Текст после получения привилегий')

    class Meta:
        db_table = "messages_new_status"

    @classmethod
    @logger.catch
    def get_messages(cls):
        data = cls.select().dicts().first()
        return data if data else {}


class GetcourseGroup(BaseModel):
    """Класс для хранения и работы с группами геткурса для бота"""
    waiting_group_id = BigIntegerField(default=0, verbose_name='id группы лист ожидания')
    club_group_id = BigIntegerField(default=0, verbose_name='id группы члены клуба')

    class Meta:
        db_table = "group_get_course"

    @classmethod
    @logger.catch
    def edit_waiting_group(cls, waiting_group_id: str):
        """Функция изменения id группы листа ожидания """
        data = cls.select().first()
        club_group_id = 0
        if data:
            club_group_id = data.club_group_id
        cls.delete().execute()
        return cls.create(waiting_group_id=waiting_group_id, club_group_id=club_group_id).save()

    @classmethod
    @logger.catch
    def edit_club_group(cls, club_group_id: int):
        """Функция изменения id группы членов клуба """
        data = cls.select().first()
        waiting_group_id = 0
        if data:
            waiting_group_id = data.waiting_group_id
        cls.delete().execute()
        return cls.create(waiting_group_id=waiting_group_id, club_group_id=club_group_id).save()

    @classmethod
    @logger.catch
    def get_waiting_group(cls) -> int:
        """Функция возвращает id канала """
        waiting_group: cls = cls.select().first()
        return waiting_group.waiting_group_id if waiting_group else 0

    @classmethod
    @logger.catch
    def get_club_group(cls) -> int:
        """Функция возвращает id группы членов клуба """
        club_group: cls = cls.select().first()
        return club_group.club_group_id if club_group else 0


class Channel(BaseModel):
    """Класс для хранения и изменения каналов и групп телеграм"""
    name = CharField(default='', verbose_name='Название канала')
    channel_id = BigIntegerField(unique=True, verbose_name='id канала')

    class Meta:
        db_table = "channels"

    @classmethod
    @logger.catch
    def add_channel(cls, channel_id: int, channel_name: str):
        """Функция добавления канала """
        return cls.get_or_create(channel_id=channel_id, name=channel_name)

    @classmethod
    @logger.catch
    def get_channels(cls) -> list:
        """Функция возвращает список каналов"""
        channels = cls.select().execute()
        return list(channels) if channels else []

    @classmethod
    @logger.catch
    def delete_channel(cls, channel_id: int) -> int:
        """Функция удаляет канал """
        return cls.delete().where(cls.channel_id == channel_id).execute()


class Group(BaseModel):
    """Клас для хранения и работы с группами"""
    group_id = IntegerField(primary_key=True, verbose_name='id группы')
    name = CharField(verbose_name='id канала')

    class Meta:
        db_table = "groups"

    @classmethod
    @logger.catch
    def edit_group(cls, groups: Tuple[dict, ...]) -> int:
        """Перезаписывает список групп"""
        for group in groups:
            group['group_id'] = group.pop('id')
        cls.delete().execute()
        return cls.insert_many(groups).execute()

    @classmethod
    @logger.catch
    def get_all_group_channel(cls) -> Tuple[tuple, ...]:
        """Возвращает список групп в виде пар кортежей """
        groups: List[cls] = list(cls.select().execute())
        return tuple((group.group_id, group.name) for group in groups)

    @classmethod
    @logger.catch
    def get_name_group_by_id(cls, group_id: int) -> str:
        """Возвращает имя группы по id """
        group: 'Group' = cls.select().where(cls.group_id == group_id).first()
        return group.name if group else 'Нет группы'


class UserStatus(BaseModel):
    """
    Model for table users_status
    Table messages for statuses
    """

    challenger = TextField(verbose_name='Сообщение подаче заявки')
    waiting = TextField(verbose_name='Сообщение при попадании в список ожидания')
    entered = TextField(verbose_name='Сообщение при вступлении в клуб')
    returned = TextField(verbose_name='Сообщение при возвращении в клуб после исключения')
    excluded = TextField(verbose_name='Сообщение при исключении из клуба')
    got_invite = TextField(verbose_name='Сообщение при повторном запросе ссылки')

    class Meta:
        db_table = "user_status"


class User(BaseModel):
    """
    Model for table users
     """
    getcourse_id = CharField(
        default=None, null=True, unique=True, verbose_name="id пользователя в getcourse")
    phone = CharField(unique=True, verbose_name="Телефон пользователя")
    telegram_id = BigIntegerField(
        unique=True, default=None, null=True, verbose_name="id пользователя в телеграмм")
    status = CharField(max_length=50, verbose_name='Статус пользователя')
    # статус обновлен
    status_updated = BooleanField(default=True, verbose_name='Обновлен статус')
    # получал инвайт ссылку
    got_invite = BooleanField(default=False, verbose_name='Получал инвайт ссылку')
    date_joining_club = DateTimeField(
        default=datetime.datetime.utcnow(), verbose_name='Дата записи о вступлении')
    expiration_date = DateTimeField(
        default=datetime.datetime.utcnow(), verbose_name='Дата окончания привилегии')

    class Meta:
        db_table = "users"

    @classmethod
    @logger.catch
    def get_list_users_for_exclude(cls: 'User', getcourse_id: tuple) -> tuple:
        """Возвращает список пользователей которых нет в последнем обновлении"""
        exclude_users = (
            cls.select().
            where(cls.getcourse_id.not_in(getcourse_id)).
            where(cls.status.in_([Statuses.entered, Statuses.returned])).execute()
        )
        return tuple(user.telegram_id for user in exclude_users if user.telegram_id)

    @classmethod
    @logger.catch
    def get_users_by_telegram_id(cls: 'User', telegram_id: int) -> 'User':
        """
        Returns User`s class instance if user with telegram_id in database else None
        return: User
        """
        return cls.get_or_none(cls.telegram_id == telegram_id)

    @classmethod
    @logger.catch
    def get_user_by_phone(cls: 'User', phone: str) -> 'User':
        """
        Поиск пользователя в базе по телефону
        """
        return cls.get_or_none(cls.phone.endswith(phone))

    @classmethod
    @logger.catch
    def update_users(cls: 'User', users: list, source: str) -> int:
        """
        Добавление отсутствующих пользователей
        или обновление данных существующих пользователей
        """
        count = 0
        if source == SourceData.club:
            for user in users:
                count += bool(cls.update_users_from_club(**user))
        elif source == SourceData.waiting_list:
            for user in users:
                count += bool(cls.update_users_from_waiting_list(**user))
        return count

    @classmethod
    @logger.catch
    def update_users_from_club(
            cls: 'User', getcourse_id: str, phone: str) -> 'User':
        """
        if the user is already in the database, returns None
        if created user will return user id
        nik_name: str
        telegram_id: str
        return: str
        """
        user = cls.get_user_by_phone(phone=phone[-10:])
        if user:
            if user.status not in [Statuses.entered, Statuses.returned]:
                new_status = Statuses.returned if user.status == Statuses.excluded else Statuses.entered
                user.getcourse_id = getcourse_id
                user.status = new_status
                user.date_joining_club = datetime.datetime.utcnow()
                user.status_updated = True
                user.save()
                return user
        else:
            result = cls.create(
                            getcourse_id=getcourse_id, phone=phone,
                            member=True, status=Statuses.entered
                        )
            return result

    @classmethod
    @logger.catch
    def update_users_from_waiting_list(
            cls: 'User', getcourse_id: str, phone: str, telegram_id: str = None) -> 'User':
        """
        if the user is already in the database, returns None
        if created user will return user id
        nik_name: str
        telegram_id: str
        return: str
        """
        user = cls.get_user_by_phone(phone=phone)
        user_by_id = cls.select().where(cls.getcourse_id == getcourse_id).first()
        if user:
            if not user.status in [Statuses.entered, Statuses.returned] and user.status != Statuses.waiting:
                user.getcourse_id = getcourse_id
                user.status = Statuses.waiting
                user.status_updated = True
                return user.save()
        elif user_by_id:
            if not user.status in [Statuses.entered, Statuses.returned] and user.status != Statuses.waiting:
                user.getcourse_id = getcourse_id
                user.status = Statuses.waiting
                user.status_updated = True
                return user.save()
        else:
            result = cls.create(
                getcourse_id=getcourse_id, telegram_id=telegram_id, phone=phone,
                member=False, status=Statuses.waiting, status_updated=True
            )
            return result

    @classmethod
    @logger.catch
    def update_privileged_user(cls: 'User') -> int:
        """
            Function updated users with status privileged
            if expiration_date < today
            set status excluded for user
        """

        return(
            cls.update({cls.status: Statuses.excluded, cls.status_updated: True}).
            where(cls.expiration_date < datetime.datetime.utcnow()).execute()
        )

    @classmethod
    @logger.catch
    def add_challenger(
            cls: 'User', phone: str, telegram_id: int) -> 'User':
        """
            function for added challenger
        """
        user = cls.get_user_by_phone(phone=phone[-10:])
        if user:
            user.telegram_id = telegram_id
            user.save()
            return user
        result = cls.create(
            telegram_id=telegram_id, phone=phone, member=False,
            status=Statuses.challenger, status_updated=True
        )
        return result

    @classmethod
    @logger.catch
    def exclude_user_by_getcourse_id(cls: 'User', getcourse_id: List[Any]) -> int:
        """
        exclude user by getcourse id
        """
        return (
          cls.update({cls.status: Statuses.excluded, cls.status_updated: True}).
          where(cls.getcourse_id.not_in(getcourse_id)).
          where(cls.status.in_([Statuses.entered, Statuses.returned])).execute()
        )

    @classmethod
    @logger.catch
    def delete_user_from_waiting_list_by_getcourse_id(cls: 'User', getcourse_id: List[Any]) -> int:
        """
        exclude user by getcourse id
        """
        return (
          cls.delete().
          where(cls.getcourse_id.not_in(getcourse_id)).
          where(cls.status == Statuses.waiting).execute()
        )

    @classmethod
    @logger.catch
    def get_users_from_waiting_list(cls: 'User') -> list:
        """
        return list of telegram ids for users from waiting list
        return: list
        """
        return [
            user.telegram_id
            for user in cls.
            select().
            where(cls.status == Statuses.waiting).
            execute() if user.telegram_id
        ]

    @classmethod
    @logger.catch
    def get_users_for_mailing_new_status(cls: 'User') -> list:
        """Получить список пользователей для рассылки"""
        users = (
            cls.select().where(cls.status_updated == True).
            where(cls.status.not_in([Statuses.challenger, Statuses.entered, Statuses.returned])).
            where(cls.telegram_id.is_null(False)).execute()
        )
        return [user for user in users if user.telegram_id]

    @classmethod
    @logger.catch
    def un_set_status_updated_except_members(cls: 'User') -> list:
        return (
            cls.update(status_updated=False).
            where(cls.status.not_in([Statuses.entered, Statuses.returned])).
            execute()
        )

    @classmethod
    @logger.catch
    def get_members_for_mailing_new_status(cls: 'User') -> list:
        """Получить список пользователей для рассылки"""
        users = (
            cls.select().where(cls.status_updated == True).
            where(cls.status.in_([Statuses.entered, Statuses.returned])).
            where(cls.date_joining_club.month < datetime.datetime.now().month).
            where(cls.status.in_([Statuses.entered, Statuses.returned])).
            where(cls.telegram_id.is_null(False)).execute()
        )
        return [user for user in users if user.telegram_id]

    @classmethod
    @logger.catch
    def un_set_status_updated_for_members(cls: 'User') -> list:
        return (
            cls.update(status_updated=False).
            where(cls.status.not_in([Statuses.entered, Statuses.returned, Statuses.challenger])).
            execute()
        )

    @classmethod
    @logger.catch
    def get_users_which_can_be_chat(cls: 'User') -> list:
        """
        return list of telegram ids for active users without admins
        return: list
        """
        return [
            user.telegram_id
            for user in cls.select(cls.telegram_id).
            where(cls.status.in_([Statuses.entered, Statuses.returned, Statuses.privileged])).
            execute() if user.telegram_id
        ]

    @classmethod
    @logger.catch
    def add_privileged_status_by_telegram_id(cls: 'User', telegram_id: int) -> bool:
        """
            function add privileged user
        """
        return (cls.update(status=Statuses.privileged, status_updated=False).
                where(cls.telegram_id == telegram_id).execute()
                )

    @classmethod
    @logger.catch
    def got_invited(cls: 'User', telegram_id: int) -> bool:
        """
            function change data got invited link
        """
        return cls.update(got_invite=True).where(cls.telegram_id == telegram_id).execute()


@logger.catch
def drop_db() -> None:
    """Deletes all tables in database"""

    with db:
        try:
            db.drop_tables([User], safe=True)
            logger.info('DB deleted')
        except Exception as err:
            logger.error(f"Ошибка удаления таблиц БД: {err}")


@logger.catch
def recreate_db(_db_file_name: str) -> None:
    """Creates new tables in database. Drop all data from DB if it exists."""

    with db:
        if os.path.exists(_db_file_name):
            drop_db()
        db.create_tables([User, Channel, Group, GetcourseGroup, UserStatus, Text, MessageNewStatus ], safe=True)
        logger.info('DB Recreated')
