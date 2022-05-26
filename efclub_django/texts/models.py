from django.db import models

# Create your models here.


class Text(models.Model):
    """Class for text message table"""
    start = models.TextField(verbose_name='Тест в основном меню')
    about = models.TextField(verbose_name='Текст о клубе')
    prices = models.TextField(verbose_name='Текст с ценами')
    reviews = models.TextField(verbose_name='Текст с отзывами')
    goodbye = models.TextField(verbose_name='Текст goodbye')
    link_waiting_list = models.CharField(max_length=255, verbose_name='Ссылка на лист ожидания')
    link_paid_excluded = models.CharField(
        max_length=255, verbose_name='Ссылка на оплату для исключенных')
    link_paid_waiting_list = models.CharField(
        max_length=255, verbose_name='Ссылка на оплату рассылки пользователям в листе ожидания')

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
    id = models.IntegerField(primary_key=True, verbose_name='id группы')
    name = models.IntegerField(verbose_name='id канала')

    class Meta:
        db_table = "groups"


class UserStatus(models.Model):
    """
    Model for table users_status
    Table messages for statuses
    """

    challenger = models.TextField(verbose_name='Сообщение подаче заявки')
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
        unique=True, default=None, null=True, verbose_name="id пользователя в телеграмм")
    status = models.CharField(max_length=50, choices=statuses, verbose_name='Статус пользователя')
    # когда статус обновлен проверяется нужно ли отправить сообщение и значение меняется на False
    status_updated = models.BooleanField(default=True, verbose_name='Обновлен статус')
    # получал инвайт ссылку
    got_invite = models.BooleanField(default=False, verbose_name='Получал инвайт ссылку')
    expiration_date = models.DateTimeField(
                                    auto_now=True, verbose_name='Дата окончания привилегии')

    class Meta:
        db_table = "users"
        verbose_name = 'пользователь'
        verbose_name_plural = u'пользователи'


class MessageNewStatus(models.Model):
    """Class for text message  table"""
    challenger = models.TextField(max_length=255, blank=True, verbose_name='Тест после отправки номера телефона')
    waiting = models.TextField(max_length=255, blank=True, verbose_name='Текст после регистрации в листе ожидания')
    entered = models.TextField(max_length=255, blank=True, verbose_name='Текст после вступления в клуб')
    returned = models.TextField(max_length=255, blank=True, verbose_name='Текст после возвращения в клуб')
    excluded = models.TextField(max_length=255, blank=True, verbose_name='Текст после исключения из клуба')
    privileged = models.CharField(max_length=255, blank=True, verbose_name='Текст после получения привилегий')

    class Meta:
        db_table = "messages_new_status"
        verbose_name = 'сообщение о новом статусе'
        verbose_name_plural = 'сообщения о новом статусе'
