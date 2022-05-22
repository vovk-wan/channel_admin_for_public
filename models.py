# import datetime
from dataclasses import dataclass
import os
from typing import Any, List, Tuple

from peewee import (CharField, BooleanField, IntegerField, TextField, ForeignKeyField, BigIntegerField)
from peewee import Model

from config import logger, db, db_file_name


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
    # got_invite: str = 'got_invite'


class BaseModel(Model):
    """A base model that will use our Sqlite database."""

    class Meta:
        database = db
        order_by = 'date_at'


class Text(BaseModel):
    """Class for text message table"""
    name = CharField(max_length=50, verbose_name='Название сообщения')
    message = TextField(verbose_name='Текст сообщения')

    class Meta:
        db_table = "text_messages"


class Channel(BaseModel):
    channel_id = CharField(default='0', verbose_name='id канала')
    group_id = CharField(default='0', verbose_name='id канала')

    class Meta:
        db_table = "channel"

    @classmethod
    @logger.catch
    def edit_channel(cls, channel_id: int):
        """Функция изменения id канала """
        data = cls.select().first()
        group_id = 0
        if data:
            group_id = data.group_id
        cls.delete().execute()
        return cls.create(channel_id=channel_id, group_id=group_id).save()

    @classmethod
    @logger.catch
    def edit_group(cls, group_id: int):
        """Функция изменения id группы """
        data = cls.select().first()
        channel_id = 0
        if data:
            channel_id = data.channel_id
        cls.delete().execute()
        return cls.create(channel_id=channel_id, group_id=group_id).save()

    @classmethod
    @logger.catch
    def get_channel(cls) -> str:
        """Функция возвращает id канала """
        channel = cls.select().first()
        return channel.channel_id if channel else ''

    @classmethod
    @logger.catch
    def get_group(cls) -> str:
        """Функция возвращает id группы """
        group = cls.select().first()
        return group.group_id if group else ''


class Group(BaseModel):
    """Клас для хранения и работы с группами"""
    id = IntegerField(verbose_name='id группы')
    name = IntegerField(verbose_name='id канала')

    class Meta:
        db_table = "groups"

    @classmethod
    @logger.catch
    def edit_group(cls, groups: Tuple[dict, ...]) -> int:
        """Перезаписывает список групп"""
        cls.delete().execute()
        return cls.insert_many(groups).execute()

    @classmethod
    @logger.catch
    def get_all_group_channel(cls) -> Tuple[tuple, ...]:
        """Возвращает список групп в виде пар кортежей """
        groups: List[cls] = list(cls.select().execute())
        return tuple((group.id, group.name) for group in groups)

    @classmethod
    @logger.catch
    def get_name_group_by_id(cls, group_id: str) -> str:
        """Возвращает имя группы по id """
        group: 'Group' = cls.get_or_none(cls.id == group_id)
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
      methods
        add_new_user
        update_users
        is_admin
        get_all_users
        get_user_by_phone
        get_users_not_admins
        get_telegram_id_users
        get_user_by_telegram_id
        set_user_status_admin
     """
    getcourse_id = CharField(
        default=None, null=True, unique=True, verbose_name="id пользователя в getcourse")
    phone = CharField(unique=True, verbose_name="id пользователя в телеграмм")
    telegram_id = BigIntegerField(
        unique=True, default=None, null=True, verbose_name="id пользователя в телеграмм")
    admin = BooleanField(default=False, verbose_name="Администраторство")
    # -------------- update
    status = CharField(max_length=50, verbose_name='Статус пользователя')
    # когда статус обновлен проверяется нужно ли отправить сообщение и значение меняется на False
    status_updated = BooleanField(default=True, verbose_name='Обновлен статус')
    # в клубе, доступ оплачен, в основной группе
    member = BooleanField(default=False, verbose_name='Член клуба')
    # получал инвайт ссылку
    got_invite = BooleanField(default=False, verbose_name='Получал инвайт ссылку')

    class Meta:
        db_table = "users"

    @classmethod
    @logger.catch
    def get_list_users_for_exclude(cls: 'User', getcourse_id: tuple) -> tuple:
        """Возвращает список пользователей которых нет в последнем обновлении"""
        exclude_users = (
            cls.select().
            where(cls.getcourse_id.not_in(getcourse_id)).
            where(cls.member == True).execute()
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
                count += bool(cls.update_users_from_club(**user, source=source))
        elif source == SourceData.waiting_list:
            for user in users:
                count += bool(cls.update_users_from_waiting_list(**user, source=source))
        return count

    @classmethod
    @logger.catch
    def update_users_from_club(
            cls: 'User', getcourse_id: str, phone: str) -> 'User':
        """
        FIXME добавлять или обновлять статус
        if the user is already in the database, returns None
        if created user will return user id
        nik_name: str
        telegram_id: str
        return: str
        """
        user = cls.get_user_by_phone(phone=phone[-10:])
        if user:
            if not user.member:
                new_status = Statuses.returned if user.status == Statuses.excluded else Statuses.entered
                user.getcourse_id = getcourse_id
                user.member = True
                user.status = new_status
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
        if user:
            if not user.member and user.status != Statuses.waiting:
                user.getcourse_id = getcourse_id
                user.member = False
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
    def delete_user_by_telegram_id(cls: 'User', telegram_id: List[Any]) -> int:
        """
        delete users by telegram id
        """
        return cls.delete().where(cls.telegram_id.in_(telegram_id)).execute()
        # user = cls.get_or_none(cls.telegram_id.in_(telegram_id))
        # if user:
        #     return user.delete_instance()

    @classmethod
    @logger.catch
    def exclude_user_by_getcourse_id(cls: 'User', getcourse_id: List[Any]) -> int:
        """
        exclude user by getcourse id
        """
        return (
          cls.update({cls.member: False, cls.status: Statuses.excluded, cls.status_updated: True}).
          where(cls.getcourse_id.not_in(getcourse_id)).
          where(cls.member == True).execute()
        )

    @classmethod
    @logger.catch
    def get_users_not_admins(cls: 'User') -> list:
        """
        return list of telegram ids for active users without admins
        return: list
        """
        return [
            user.telegram_id
            for user in cls.select(cls.telegram_id)
                .where(cls.admin == False).where(cls.member == True).execute() if user.telegram_id
        ]

    @classmethod
    @logger.catch
    def set_user_status_admin(cls: 'User', telegram_id: str) -> bool:
        """
        set admin value enabled for user
        return: 1 if good otherwise 0
        """
        return cls.update(admin=True).where(cls.telegram_id == telegram_id).execute()

    @classmethod
    @logger.catch
    def delete_status_admin(cls: 'User', telegram_id: str) -> int:
        """
        set admin value enabled for user
        return: 1 if good otherwise 0
        """
        return cls.update(admin=False).where(cls.telegram_id == telegram_id).execute()

    @classmethod
    @logger.catch
    def is_admin(cls: 'User', telegram_id: str) -> bool:
        """
        checks if the user is an administrator
        return: bool
        """
        user = cls.get_or_none(cls.telegram_id == telegram_id)
        return user.admin if user else False


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
        db.create_tables([User, Channel, Group, UserStatus, Text], safe=True)
        logger.info('DB Recreated')


if __name__ == '__main__':
    # test()
    recreate = 1
    add_test_users = 1
    add_admins = 0
    import random
    import string
    test_user_list = (
        (f'test{user}', ''.join(random.choices(string.ascii_letters, k=5)))
        for user in range(1, 6))

    if recreate:
        recreate_db(db_file_name)
