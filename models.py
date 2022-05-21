# import datetime
from dataclasses import dataclass
import os
from typing import Any, List, Tuple

from peewee import (CharField, BooleanField, IntegerField, TextField, ForeignKeyField)
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
        """Функция возвращает id канала """
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
        delete_user_by_telegram_id
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
    telegram_id = CharField(
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
    def get_list_users_for_kicked(cls: 'User', getcourse_id: tuple) -> tuple:
        """Возвращает список пользователей которых нет в последнем обновлении"""
        kicked_user = cls.select().where(cls.getcourse_id.not_in(getcourse_id)).execute()

        return tuple(user.telegram_id for user in kicked_user if user.telegram_id)

    @classmethod
    @logger.catch
    def get_users_by_telegram_id(cls: 'User', telegram_id: str) -> 'User':
        """
        Returns User`s class instance if user with telegram_id in database else None

        if the user is already in the database, returns the user
        otherwise it will return none

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
    def update_users(cls: 'User', users: list) -> int:
        """
        Добавление отсутствующих пользователей
        """
        count = 0
        for user in users:
            count += bool(cls.add_new_user(**user))
        return count

    @classmethod
    @logger.catch
    def add_new_user(
            cls: 'User',
            getcourse_id: str,
            phone: str,
            telegram_id: str = None,
    ) -> str:
        """
        if the user is already in the database, returns None
        if created user will return user id
        nik_name: str
        telegram_id: str
        proxy: str
        expiration: int  (hours)
        return: str
        """
        user = cls.get_or_none(cls.getcourse_id == getcourse_id)
        if not user:
            result = cls.create(
                            getcourse_id=getcourse_id, telegram_id=telegram_id, phone=phone
                        ).save()

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
    def delete_user_by_getcourse_id(cls: 'User', getcourse_id: List[Any]) -> int:
        """
        delete user by getcourse id
        """
        return cls.delete().where(cls.getcourse_id.not_in(getcourse_id)).execute()

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
                .where(cls.admin == False) if user.telegram_id
        ]

    @classmethod
    @logger.catch
    def get_all_users(cls: 'User') -> dict:
        """
        returns dict of all users
        return: dict
        """
        return {
            user.telegram_id: (
                f'{user.getcourse_id} | '
                f'{"Admin" if user.admin else "Not admin"} | '
                f'\nID: {user.telegram_id if user.telegram_id else "ЧТО ТО СЛОМАЛОСЬ"} | '
                )
            for user in User.select().execute()
        }

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
    def delete_status_admin(cls: 'User', telegram_id: str) -> bool:
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
        db.create_tables([User, Channel, Group], safe=True)
        logger.info('DB REcreated')


if __name__ == '__main__':
    # test()
    recreate = 1
    add_test_users = 0
    add_admins = 0
    add_tokens = 0
    set_proxy = 0
    import random
    import string
    test_user_list = (
        (f'test{user}', ''.join(random.choices(string.ascii_letters, k=5)))
        for user in range(1, 6))

    if recreate:
        recreate_db(db_file_name)
