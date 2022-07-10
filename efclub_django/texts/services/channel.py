from django.db.models import QuerySet

from efclub_django.settings import logger
from texts.models import Channel


class DBIChannel:
    model = Channel

    @classmethod
    @logger.catch
    def add_channel(cls, channel_id: int, name: str) -> tuple['Channel', bool]:
        """Функция добавления канала """
        return cls.model.objects.get_or_create(channel_id=channel_id, name=name)

    @classmethod
    @logger.catch
    def get_channels(cls) -> QuerySet:
        """Функция возвращает список каналов"""
        channels = cls.model.objects.all()
        return channels

