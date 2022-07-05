from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, views
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from texts.models import User, UserStatus, Group, GetcourseGroup, MessageNewStatus
from texts.serializers import (
    UserSerializerModel,
    UpdateUserSerializerModel,
    TelegramIDSerializerModel,
    MailingSerializerModel, SetGroupIdSerializerModel
)
from texts.services.getcourse_group import DBIGetcourseGroup
from texts.services.user import DBIUser
from texts.services.group import DBIGroup

from django.conf import settings


class UpdateUsersViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = UpdateUserSerializerModel
    model = User
    queryset = User.objects.all()
    source = ''

    def create(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            data = [data]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        added = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'added_users': added}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return DBIUser.update_users(serializer.data, source=self.source)
        # serializer.save()

    def get(self, request, *args, **kwargs):
        source = kwargs.get('source', '')
        return self.list(request, many=True, source=source)

    def post(self, request, *args, **kwargs):
        self.source = kwargs.get('source', '')
        return self.create(request, many=True)


# class UsersForExcludeViewSet(ListModelMixin, GenericAPIView):
#     serializer_class = TelegramIDSerializerModel
#     queryset = DBIUser.get_list_users_for_exclude()
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         serializer = self.get_serializer(queryset, many=True)
#         users = serializer.data
#         data = [user.get('telegram_id') for user in users]
#         return Response(status=status.HTTP_200_OK, data=data)
#
#     def get(self, request):
#         return self.list(request)


class GetExcludeUsersViewSet(ListModelMixin, GenericAPIView):
    serializer_class = TelegramIDSerializerModel
    queryset = DBIUser.get_list_users_for_exclude()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        users = serializer.data
        data = [user.get('telegram_id') for user in users]
        return Response(status=status.HTTP_200_OK, data=data)

    def get(self, request):
        return self.list(request)


class GetUsersForMailingNewStatusViewSet(ListModelMixin, GenericAPIView):
    serializer_class = MailingSerializerModel
    queryset = DBIUser.get_users_for_mailing_new_status()
    model = User

    def get(self, request):
        return self.list(request)


class GetMembersForMailingNewStatusViewSet(ListModelMixin, GenericAPIView):
    serializer_class = MailingSerializerModel
    queryset = DBIUser.get_members_for_mailing_new_status()
    model = User

    def get(self, request):
        return self.list(request)


class RemovesStatusUpdatedUsersViewSet(views.APIView):
    def get(self, request):
        result = DBIUser.un_set_status_updated_except_members()
        return Response(status=status.HTTP_200_OK, data={'updated_users': result})


class RemovesStatusUpdatedMembersViewSet(views.APIView):
    def get(self, request):
        result = DBIUser.un_set_status_updated_for_members()
        return Response(status=status.HTTP_200_OK, data={'updated_users': result})


class GetGroupViewSet(views.APIView):
    def get(self, request, *args, **kwargs):
        group_name = kwargs.get('group')
        result = DBIGetcourseGroup.get_group(group_name=group_name)
        return Response(status=status.HTTP_200_OK, data=result)


class SetGroupViewSet(GenericAPIView):
    serializer_class = SetGroupIdSerializerModel
    def post(self, request, *args, **kwargs):
        group_name = kwargs.get('group_name')
        group_id = request.data.get('group_id')
        result = DBIGetcourseGroup.set_group(group_id=group_id, group_name=group_name)
        return Response(status=status.HTTP_200_OK, data=result)

    def get(self, request, *args, **kwargs):
        return Response()


class UpdateFromGetcourse(views.APIView):
    def get(self, request):
        settings.LOGGER.info('мы тута')
        return Response(status=status.HTTP_200_OK, data={'result': 'ok'})


class BookViewSet(ListModelMixin, GenericAPIView):
    serializer_class = UserSerializerModel
    # pagination_class = MyResultsSetPagination

    def get_queryset(self):
        queryset = User.objects.all()
        #
        # if name := self.request.query_params.get('name'):
        #     queryset = queryset.filter(name=name)
        #
        # if author_name := self.request.query_params.get('author_name'):
        #     queryset = queryset.filter(author__name=author_name)
        #
        # if pages_min := self.request.query_params.get('pages_min'):
        #     queryset = queryset.filter(number_pages__gte=pages_min)
        #
        # if pages_max := self.request.query_params.get('pages_max'):
        #     queryset = queryset.filter(number_pages__lte=pages_max)
        #
        # if pages := self.request.query_params.get('pages'):
        #     queryset = queryset.filter(number_pages=pages)

        return queryset

    def get(self, request):
        return self.list(request.data)

