from dataclasses import dataclass
from django.forms.models import model_to_dict
from efclub_django.settings import logger
from text.models import MessageNewStatus


class DBIMessageNewStatus(MessageNewStatus):

    @classmethod
    @logger.catch
    def get_messages(cls: MessageNewStatus):
        data = cls.objects.first()
        return model_to_dict(data, fields=[field.name for field in data._meta.fields]) if data else {}
