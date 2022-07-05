import datetime
from efclub_django.settings import logger
from texts.models import Statuses, SourceData, User
from django.db.models.query import QuerySet


class DBIUser:
    model = User

    @classmethod
    @logger.catch
    def get_list_users_for_exclude(cls: 'DBIUser', getcourse_id: tuple = tuple()) -> QuerySet:
        """
        Returns a list of users who are not present in the latest update
        """

        exclude_users = (
            cls.model.objects.
            only('telegram_id').
            exclude(getcourse_id__in=getcourse_id).
            filter(status__in=[Statuses.entered, Statuses.returned]).
            filter(telegram_id__isnull=False).all()
        )
        return exclude_users

    @classmethod
    @logger.catch
    def get_users_by_telegram_id(cls: 'DBIUser', telegram_id: int) -> 'User':
        """
        Returns User`s class instance if user with telegram_id in database else None
        return: User
        """
        return cls.model.objects.filter(telegram_id=telegram_id).first()

    @classmethod
    @logger.catch
    def get_user_by_phone(cls: 'DBIUser', phone: str) -> 'User':
        """
        Search for users by phone in the database
        """
        return cls.model.objects.filter(phone__endswith=phone[-10:]).first()

    @classmethod
    @logger.catch
    def update_users(cls: 'DBIUser', users: list, source: str) -> int:
        """
        Adding new users and updating data for users in the list
        """
        count = 0
        if source == SourceData.club:
            cls.exclude_user_by_getcourse_id([user.get('getcourse_id') for user in users])
            for user in users:

                count += bool(cls.update_users_from_club(**user))
        elif source == SourceData.waiting_list:
            for user in users:
                count += bool(cls.update_users_from_waiting_list(**user))
        return count

    @classmethod
    @logger.catch
    def update_users_from_club(cls: 'DBIUser', getcourse_id: str, phone: str, **kwargs) -> 'User':
        """
        if the user is already in the database, returns None
        if created user will return user id
        nik_name: str
        telegram_id: str
        return: str
        """
        user = cls.get_user_by_phone(phone=phone[-10:])
        user_by_id = cls.model.objects.filter(getcourse_id=getcourse_id).first()
        if user:
            if user.status not in [Statuses.entered, Statuses.returned]:
                new_status = Statuses.returned if user.status == Statuses.excluded else Statuses.entered
                user.status_updated = new_status != user.status
                user.getcourse_id = getcourse_id
                user.phone = phone
                user.status = new_status
                user.date_joining_club = datetime.datetime.utcnow()
                user.save()
                return user
        elif user_by_id:
            if user_by_id.status not in [Statuses.entered, Statuses.returned]:
                user_by_id.getcourse_id = getcourse_id
                new_status = Statuses.returned if user_by_id.status == Statuses.excluded else Statuses.entered
                user_by_id.status_updated = new_status != user_by_id.status
                user_by_id.status = new_status
                user_by_id.phone = phone
                user_by_id.save()
                return user_by_id
            elif user_by_id.phone != phone:
                user_by_id.phone = phone
                user_by_id.save()
        else:
            result = cls.model.objects.create(
                getcourse_id=getcourse_id, phone=phone,
                status=Statuses.entered
            )
            return result

    @classmethod
    @logger.catch
    def update_users_from_waiting_list(
            cls: 'DBIUser', getcourse_id: str, phone: str, telegram_id: str = None, **kwargs) -> 'User':
        """
        if the user is already in the database, returns None
        if created user will return user id
        nik_name: str
        telegram_id: str
        return: str
        """
        user = cls.get_user_by_phone(phone=phone[-10:])
        user_by_id = cls.model.objects.filter(getcourse_id=getcourse_id).first()
        if user:
            if user.status not in [Statuses.entered, Statuses.returned, Statuses.excluded]:
                user.getcourse_id = getcourse_id
                user.status_updated = user.status != Statuses.waiting
                user.status = Statuses.waiting
                user.phone = phone
                user.save()
                return user
        elif user_by_id:
            if not user_by_id.status in [Statuses.entered, Statuses.returned, Statuses.excluded]:
                user_by_id.getcourse_id = getcourse_id
                user_by_id.status_updated = user_by_id.status != Statuses.waiting
                user_by_id.status = Statuses.waiting
                user_by_id.phone = phone
                user_by_id.save()
                return user_by_id
        else:
            result = cls.model.objects.create(
                getcourse_id=getcourse_id, telegram_id=telegram_id, phone=phone,
                status=Statuses.waiting, status_updated=True
            )
            return result

    @classmethod
    @logger.catch
    def add_challenger(cls: 'DBIUser', phone: str, telegram_id: int) -> 'User':
        """
            function for added challenger
        """
        user = cls.get_user_by_phone(phone=phone[-10:])
        if user:
            user.telegram_id = telegram_id
            user.save()
            return user
        result = cls.model.objects.create(
            telegram_id=telegram_id, phone=phone,
            status=Statuses.challenger, status_updated=True
        )
        return result

    @classmethod
    @logger.catch
    def exclude_user_by_getcourse_id(cls: 'DBIUser', getcourse_id: list) -> int:
        """
        exclude user by getcourse id
        """
        return (
            cls.model.objects.exclude(getcourse_id__in=getcourse_id).
            filter(status__in=[Statuses.entered, Statuses.returned]).
            update(status=Statuses.excluded, status_updated=True)
        )

    @classmethod
    @logger.catch
    def delete_user_from_waiting_list_by_getcourse_id(cls: 'DBIUser', getcourse_id: list) -> int:
        """
        exclude user by getcourse id
        """
        return (
            cls.model.objects.
            exclude(getcourse_id__in=getcourse_id).
            filter(status=Statuses.waiting).all().delete()
        )

    @classmethod
    @logger.catch
    def get_users_from_waiting_list(cls: 'DBIUser') -> list:
        """
        return list of telegram ids for users from waiting list
        return: list
        """
        return [
            user.telegram_id
            for user in cls.model.objects.filter(status=Statuses.waiting).
            filter(telegram_id__isnull=False).all()
        ]

    @classmethod
    @logger.catch
    def get_users_for_mailing_new_status(cls: 'DBIUser') -> QuerySet:
        """Получить список пользователей для рассылки"""
        users = (
            cls.model.objects.only('telegram_id', 'got_invite', 'status').
                exclude(status__in=[Statuses.challenger, Statuses.entered, Statuses.returned]).
                filter(status_updated=True).filter(telegram_id__isnull=False).
            all()
        )
        return users

    @classmethod
    @logger.catch
    def un_set_status_updated_except_members(cls: 'DBIUser') -> int:
        """
        Removes the "updated" status for users excluding entered and returned.
        """
        return (
            cls.model.objects.
            filter(status__in=[Statuses.challenger, Statuses.waiting, Statuses.excluded]).
            filter(status_updated=True).all().
            update(status_updated=False)
        )


    @classmethod
    @logger.catch
    def get_members_for_mailing_new_status(cls: 'DBIUser') -> QuerySet:
        """
        Getting users for mailing excluding entered and returned.
        """
        users = (
            cls.model.objects.only('telegram_id', 'got_invite', 'status').
                filter(status__in=[Statuses.entered, Statuses.returned]).
                filter(status_updated=True).filter(telegram_id__isnull=False).
                filter(date_joining_club__month__lt=datetime.datetime.now().month).
                all()
        )
        return users
        # users = (
        #     cls.model.objects.filter(status_updated=True).
        #     filter(status__in=[Statuses.entered, Statuses.returned]).
        #     filter(date_joining_club__month__lt=datetime.datetime.now().month).
        #     filter(telegram_id__isnull=False).all()
        # )
        # return [user for user in users]

    @classmethod
    @logger.catch
    def un_set_status_updated_for_members(cls: 'DBIUser') -> list:
        """
        Removes the "updated" status for members club.
        """
        return (
            cls.model.objects.filter(status_updated=True).
            filter(status__in=[Statuses.entered, Statuses.returned]).
            filter(date_joining_club__month__lt=datetime.datetime.now().month).
            filter(telegram_id__isnull=False).all().update(status_updated=False)
        )

    @classmethod
    @logger.catch
    def get_users_which_can_be_chat(cls: 'DBIUser') -> list:
        """
        Return list of telegram ids for active users without admins
        return: list
        """
        return [
            user.telegram_id
            for user in cls.model.objects.only('telegram_id').
            filter(status__in=[Statuses.entered, Statuses.returned, Statuses.privileged]).
            filter(telegram_id__isnull=False).all()
        ]

    @classmethod
    @logger.catch
    def add_privileged_status_by_telegram_id(cls: 'DBIUser', telegram_id: int) -> bool:
        """
            function add privileged user
        """
        return (
            cls.model.objects.filter(telegram_id=telegram_id).all().
            update(status=Statuses.privileged, status_updated=False)
                )

    @classmethod
    @logger.catch
    def got_invited(cls: 'DBIUser', telegram_id: int) -> bool:
        """
            function change data got invited link
        """
        return cls.model.objects.filter(telegram_id=telegram_id).all().update(got_invite=True)
