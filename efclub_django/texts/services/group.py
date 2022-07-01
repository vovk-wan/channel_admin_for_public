
from efclub_django.settings import logger
from text.models import Group


class DBIGroup(Group):

    @classmethod
    @logger.catch
    def edit_group(cls, groups: tuple[dict, ...]) -> int:
        """Перезаписывает список групп"""
        for group in groups:
            group['group_id'] = group.pop('id')
        groups = [cls(group) for group in groups]
        cls.objects.all().delete()
        return cls.objects.bulk_create(groups)

    @classmethod
    @logger.catch
    def get_all_group_channel(cls) -> tuple[tuple, ...]:
        """Возвращает список групп в виде пар кортежей """
        groups: list['Group'] = list(cls.objects.all())
        return tuple((group.group_id, group.name) for group in groups)

    @classmethod
    @logger.catch
    def get_name_group_by_id(cls, group_id: int) -> str:
        """Возвращает имя группы по id """
        group: 'Group' = cls.objects.filter(group_id=group_id).first()
        return group.name if group else 'Нет группы'
