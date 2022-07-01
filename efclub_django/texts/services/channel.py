
from efclub_django.settings import logger
from text.models import Channel


class DBIChannel(Channel):

    @classmethod
    @logger.catch
    def add_channel(cls, channel_id: int, channel_name: str):
        """Функция добавления канала """
        return cls.objects.get_or_create(channel_id=channel_id, name=channel_name)

    @classmethod
    @logger.catch
    def get_channels(cls) -> list:
        """Функция возвращает список каналов"""
        channels = cls.objects.execute()
        return list(channels) if channels else []

    @classmethod
    @logger.catch
    def delete_channel(cls, channel_id: int) -> int:
        """Функция удаляет канал """
        return cls.objects.filter(channel_id=channel_id).delete()
