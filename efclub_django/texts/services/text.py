from dataclasses import dataclass
from django.forms.models import model_to_dict
from efclub_django.settings import logger
from texts.models import (
    UserStatus, Channel, Group, GetcourseGroup, Text, DefaultTexts, )


class DBIText:
    model = Text

    @classmethod
    @logger.catch
    def get_start_text(cls):
        """Возвращает текст в основном меню"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.start if data.start else 'no text'

    @classmethod
    @logger.catch
    def get_about_text(cls):
        """Возвращает Текст о клубе"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.about

    @classmethod
    @logger.catch
    def get_prices_text(cls):
        """Возвращает Текст с ценами"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.prices

    @classmethod
    @logger.catch
    def get_reviews_text(cls):
        """Возвращает Текст с отзывами"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.reviews

    @classmethod
    @logger.catch
    def get_for_mailing_text(cls):
        """Возвращает Текст в рассылки на оплату"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.for_mailing

    @classmethod
    @logger.catch
    def get_for_invite_text(cls):
        """Возвращает Текст вместе с инвайт ссылками"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.for_invite

    @classmethod
    @logger.catch
    def get_want_for_get_phone_text(cls):
        """Возвращает Текст с запросом контакта"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.for_get_phone

    @classmethod
    @logger.catch
    def get_want_for_challenger_text(cls):
        """Возвращает "Хочу в клуб" новичков"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.for_challenger

    @classmethod
    @logger.catch
    def get_want_for_waiting_list_text(cls):
        """Возвращает "Хочу в клуб" для листа ожидания"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.for_waiting_list

    @classmethod
    @logger.catch
    def get_want_for_excluded_text(cls):
        """Возвращает "Хочу в клуб" исключенных"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.for_excluded

    @classmethod
    @logger.catch
    def get_want_for_entered_text(cls):
        """Возвращает "Хочу в клуб" для тех кто может получить ссылку"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.for_entered

    @classmethod
    @logger.catch
    def get_want_for_entered_got_link_text(cls):
        """Возвращает "Хочу в клуб" для тех кто уже получал ссылку"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.for_entered_got_link

    @classmethod
    @logger.catch
    def get_link_waiting_list_text(cls):
        """Возвращает ссылку в лист ожидания"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.link_waiting_list

    @classmethod
    @logger.catch
    def get_link_to_pay(cls):
        """Возвращает ссылку на оплату"""
        data = cls.model.objects.first()
        if not data:
            data = DefaultTexts
        return data.link_to_pay
