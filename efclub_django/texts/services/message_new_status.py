from dataclasses import dataclass
from django.forms.models import model_to_dict
from efclub_django.settings import logger
from texts.models import MessageNewStatus


class DBIMessageNewStatus:
    model = MessageNewStatus

    @classmethod
    @logger.catch
    def get_messages(cls: 'DBIMessageNewStatus'):
        data = cls.model.objects.first()
        return model_to_dict(data, fields=[field.name for field in data._meta.fields]) if data else {}
