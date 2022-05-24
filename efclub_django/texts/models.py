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

    class Meta:
        db_table = "text_messages"


class GetcourseGroup(models.Model):
    waiting_group_id = models.CharField(
        max_length=255, default='0', verbose_name='id группы лист ожидания')
    club_group_id = models.CharField(
        max_length=255, default='0', verbose_name='id группы члены клуба')

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
    getcourse_id = models.CharField(
        max_length=255,
        default=None,
        null=True,
        unique=True,
        verbose_name="id пользователя в getcourse"
    )
    phone = models.CharField(max_length=255, unique=True, verbose_name="id пользователя в телеграмм")
    telegram_id = models.BigIntegerField(
        unique=True, default=None, null=True, verbose_name="id пользователя в телеграмм")
    admin = models.BooleanField(default=False, verbose_name="Администраторство")
    # -------------- update
    status = models.CharField(max_length=50, verbose_name='Статус пользователя')
    # когда статус обновлен проверяется нужно ли отправить сообщение и значение меняется на False
    status_updated = models.BooleanField(default=True, verbose_name='Обновлен статус')
    # в клубе, доступ оплачен, в основной группе
    member = models.BooleanField(default=False, verbose_name='Член клуба')
    # получал инвайт ссылку
    got_invite = models.BooleanField(default=False, verbose_name='Получал инвайт ссылку')
    expiration_date = models.DateTimeField(
                                    auto_now=True, verbose_name='Дата окончания привилегии')

    class Meta:
        db_table = "users"
