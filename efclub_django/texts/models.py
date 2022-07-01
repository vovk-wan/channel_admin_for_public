import datetime
from dataclasses import dataclass

import django.utils.timezone
from django.db import models


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


class Text(models.Model):
    """Class for text message table"""
    start = models.TextField(verbose_name='Текст в основном меню')
    about = models.TextField(verbose_name='Текст о клубе')
    prices = models.TextField(verbose_name='Текст с ценами')
    reviews = models.TextField(verbose_name='Текст с отзывами')
    for_mailing = models.TextField(verbose_name='Текст в рассылки на оплату')
    for_invite = models.TextField(verbose_name='Текст вместе с инвайт ссылками')
    for_get_phone = models.TextField(verbose_name='Текст с запросом контакта')
    for_challenger = models.TextField(verbose_name='"Хочу в клуб" новичков')
    for_waiting_list = models.TextField(verbose_name='"Хочу в клуб" для листа ожидания')
    for_excluded = models.TextField(verbose_name='"Хочу в клуб" исключенных')
    for_entered = models.TextField(verbose_name='"Хочу в клуб" для тех кто может получить ссылку')
    for_entered_got_link = models.TextField(verbose_name='"Хочу в клуб" для тех кто уже получал ссылку')

    link_waiting_list = models.CharField(max_length=255, verbose_name='Ссылка на лист ожидания')
    link_to_pay = models.CharField(
        max_length=255, verbose_name='Ссылка на оплату')

    class Meta:
        db_table = "text_messages"
        verbose_name = 'Текст в меню'
        verbose_name_plural = 'Тексты в меню'


class GetcourseGroup(models.Model):
    waiting_group_id = models.CharField(
        max_length=255, default='', verbose_name='id группы лист ожидания')
    club_group_id = models.CharField(
        max_length=255, default='', verbose_name='id группы члены клуба')

    class Meta:
        db_table = "group_get_course"


class Channel(models.Model):
    name = models.CharField(max_length=255, default='', verbose_name='id канала')
    channel_id = models.BigIntegerField(unique=True, verbose_name='id канала')

    class Meta:
        db_table = "channels"


class Group(models.Model):
    """Клас для хранения и работы с группами"""
    group_id = models.IntegerField(primary_key=True, verbose_name='id группы')
    name = models.CharField(max_length=255, verbose_name='id канала')

    class Meta:
        db_table = "groups"


class UserStatus(models.Model):
    """
    Model for table users_status
    Table messages for statuses
    """
    waiting = models.TextField(verbose_name='Сообщение при попадании в список ожидания')
    entered = models.TextField(verbose_name='Сообщение при вступлении в клуб')
    returned = models.TextField(verbose_name='Сообщение при возвращении в клуб после исключения')
    excluded = models.TextField(verbose_name='Сообщение при исключении из клуба')
    got_invite = models.TextField(verbose_name='Сообщение при повторном запросе ссылки')

    class Meta:
        db_table = "user_status"


class User(models.Model):
    """
    Model for table users
     """
    statuses = [
        ('challenger', 'претендент'),
        ('waiting', 'В листе ожидания'),
        ('excluded', 'исключен'),
        ('entered', 'Вступил'),
        ('returned', 'Вернулся после исключения'),
        ('privileged', 'Привилегированный'),
    ]
    getcourse_id = models.CharField(
        max_length=255,
        default=None,
        blank=True,
        null=True,
        unique=True,
        verbose_name="id пользователя в getcourse"
    )
    phone = models.CharField(max_length=255, unique=True, verbose_name="телефон")
    telegram_id = models.BigIntegerField(
        unique=True, default=None, null=True, blank=True, verbose_name="id пользователя в телеграмм")
    status = models.CharField(max_length=50, choices=statuses, verbose_name='Статус пользователя')
    # когда статус обновлен проверяется нужно ли отправить сообщение и значение меняется на False
    status_updated = models.BooleanField(default=True, verbose_name='Обновлен статус')
    # получал инвайт ссылку
    got_invite = models.BooleanField(default=False, verbose_name='Получал инвайт ссылку')
    expiration_date = models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата окончания привилегии')
    date_joining_club = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи о вступлении')

    class Meta:
        db_table = "users"
        verbose_name = 'пользователь'
        verbose_name_plural = u'пользователи'


class MessageNewStatus(models.Model):
    """Class for text message  table"""
    waiting = models.TextField(blank=True, verbose_name='Текст после регистрации в листе ожидания')
    entered = models.TextField(blank=True, verbose_name='Текст после вступления в клуб')
    returned = models.TextField(blank=True, verbose_name='Текст после возвращения в клуб')
    excluded = models.TextField(blank=True, verbose_name='Текст после исключения из клуба')
    privileged = models.TextField(blank=True, verbose_name='Текст после получения привилегий')

    class Meta:
        db_table = "messages_new_status"
        verbose_name = 'сообщение о новом статусе'
        verbose_name_plural = 'сообщения о новом статусе'
