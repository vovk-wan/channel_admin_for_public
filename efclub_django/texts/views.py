from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404, GenericAPIView, CreateAPIView, views, UpdateAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin

from texts.models import User, UserStatus, Group, GetcourseGroup, MessageNewStatus
from texts.serializers import (
    UserSerializerModel,
    UpdateUserSerializerModel,
    TelegramIDSerializerModel,
    MailingSerializerModel, SetGroupIdSerializerModel,
    GetUserSerializerModel, ChallengerSerializerModel, GotInvitedSerializerModel
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
    model = DBIUser.model

    def get(self, request):
        return self.list(request)


class GetUsersForWaitingListWithTelegramIdViewSet(ListModelMixin, GenericAPIView):
    serializer_class = MailingSerializerModel
    queryset = DBIUser.get_users_from_waiting_list()
    model = DBIUser.model

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


class GetUserByTelegramIDViewSet(RetrieveModelMixin, GenericAPIView):
    serializer_class = GetUserSerializerModel

    def get_object(self):
        telegram_id = self.kwargs.get('telegram_id')
        return DBIUser.get_users_by_telegram_id(telegram_id=telegram_id)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request)


# class UpdateFromGetcourse(views.APIView):
#     def get(self, request):
#         settings.LOGGER.info('мы тута')
#         return Response(status=status.HTTP_200_OK, data={'result': 'ok'})


class AddChallengerViewSet(CreateAPIView, GenericAPIView):
    serializer_class = ChallengerSerializerModel
    interface = DBIUser

    def perform_create(self, serializer):
        self.interface.add_challenger(**serializer.data)


class GotInvitedViewSet(RetrieveUpdateAPIView):
    serializer_class = GotInvitedSerializerModel
    interface = DBIUser

    def get_object(self):
        self.request.data['got_invite'] = True
        telegram_id = self.kwargs.get('telegram_id')
        instance = get_object_or_404(self.interface.model.objects,telegram_id=telegram_id)
        return instance

