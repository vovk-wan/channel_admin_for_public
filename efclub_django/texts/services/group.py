from efclub_django.settings import logger
from texts.models import Group


class DBIGroup:
    model = Group

    @classmethod
    @logger.catch
    def edit_group(cls, groups: tuple[dict, ...]):
        """Перезаписывает список групп"""
        for group in groups:
            group['group_id'] = group.pop('id')
        groups = [cls.model(**group) for group in groups]
        cls.model.objects.all().delete()
        return cls.model.objects.bulk_create(groups)

    @classmethod
    @logger.catch
    def get_all_group(cls) -> tuple[tuple, ...]:
        """Возвращает список групп в виде пар кортежей """
        groups: list['Group'] = list(cls.model.objects.all())
        return tuple((group.group_id, group.name) for group in groups)

    @classmethod
    @logger.catch
    def get_name_group_by_id(cls, group_id: int) -> str:
        """Возвращает имя группы по id """
        group: 'Group' = cls.model.objects.filter(group_id=group_id).first()
        return group.name if group else 'Нет группы'
