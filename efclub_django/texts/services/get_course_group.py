from efclub_django.settings import logger
from text.models import GetcourseGroup


class DBIGetcourseGroup(GetcourseGroup):

    @classmethod
    @logger.catch
    def edit_waiting_group(cls, waiting_group_id: str):
        """Функция изменения id группы листа ожидания """
        data = cls.objects.first()
        club_group_id = 0
        if data:
            club_group_id = data.club_group_id
        cls.objects.all().delete()
        return cls.objects.create(waiting_group_id=waiting_group_id, club_group_id=club_group_id).save()

    @classmethod
    @logger.catch
    def edit_club_group(cls, club_group_id: int):
        """Функция изменения id группы членов клуба """
        data = cls.objects.first()
        waiting_group_id = 0
        if data:
            waiting_group_id = data.waiting_group_id
        cls.objects.all().delete()
        return cls.objects.create(waiting_group_id=waiting_group_id, club_group_id=club_group_id).save()

    @classmethod
    @logger.catch
    def get_waiting_group(cls) -> int:
        """Функция возвращает id канала """
        waiting_group: cls = cls.objects.first()
        return waiting_group.waiting_group_id if waiting_group else 0

    @classmethod
    @logger.catch
    def get_club_group(cls) -> int:
        """Функция возвращает id группы членов клуба """
        club_group: cls = cls.objects.first()
        return club_group.club_group_id if club_group else 0
