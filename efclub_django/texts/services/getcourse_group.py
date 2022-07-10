from efclub_django.settings import logger
from texts.models import GetcourseGroup, Group


class DBIGetcourseGroup:
    model = GetcourseGroup

    @classmethod
    @logger.catch
    def edit_waiting_group(cls, waiting_group_id: str):
        """Функция изменения id группы листа ожидания """
        data = cls.model.objects.first()
        club_group_id = 0
        if data:
            club_group_id = data.club_group_id
        cls.model.objects.all().delete()
        cls.model.objects.create(waiting_group_id=waiting_group_id, club_group_id=club_group_id).save()

    @classmethod
    @logger.catch
    def edit_club_group(cls, club_group_id: str):
        """Функция изменения id группы членов клуба """
        data = cls.model.objects.first()
        waiting_group_id = 0
        if data:
            waiting_group_id = data.waiting_group_id
        cls.model.objects.all().delete()
        return cls.model.objects.create(waiting_group_id=waiting_group_id, club_group_id=club_group_id).save()

    @classmethod
    @logger.catch
    def get_group(cls, ) -> dict:
        """Функция изменения id группы """
        data: cls.model = cls.model.objects.first()
        if data:
            waiting_group = Group.objects.filter(group_id=data.waiting_group_id).first()
            club_group = Group.objects.filter(group_id=data.club_group_id).first()
            club_group = club_group.name if club_group else 'Не выбрано.'
            waiting_group = waiting_group.name if waiting_group else 'Не выбрано.'
            result = {
                'waiting_group': {'id': data.waiting_group_id, 'name': waiting_group},
                'club_group': {'id': data.club_group_id, 'name': club_group},
            }
            return result
        result = {
            'waiting_group': {'id': 0, 'name': 'Не выбрано.'},
            'club_group': {'id': 0, 'name': 'Не выбрано.'},
        }
        return result

    @classmethod
    @logger.catch
    def set_group(cls, group_id: str, group_name: str):
        """Функция изменения id группы """
        data: cls.model = cls.model.objects.first()
        if data:
            if group_name == 'waiting_list':
                data.waiting_group_id = group_id
            if group_name == 'club':
                data.club_group_id = group_id
            data.save()
            return {'result': True}
        waiting_group_id = group_id if group_name == 'waiting_list' else 0
        club_group_id = group_id if group_name == 'club' else 0

        cls.model.objects.create(waiting_group_id=waiting_group_id, club_group_id=club_group_id).save()
        return {'result': True}

    @classmethod
    @logger.catch
    def get_waiting_group(cls) -> int:
        """Функция возвращает id канала """
        waiting_group: cls.model = cls.model.objects.first()
        return waiting_group.waiting_group_id if waiting_group else 0

    @classmethod
    @logger.catch
    def get_club_group(cls) -> int:
        """Функция возвращает id группы членов клуба """
        club_group: cls.model = cls.model.objects.first()
        return club_group.club_group_id if club_group else 0
