from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404, GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from texts.models import User, UserStatus, Group, GetcourseGroup, MessageNewStatus
from texts.serializers import (
    GroupSerializerModel,
)
from texts.services.getcourse_group import DBIGetcourseGroup
from texts.services.group import DBIGroup
from texts.services.group import DBIGroup

from django.conf import settings


# class UpdateUsersViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
#     serializer_class = UpdateUserSerializerModel
#     model = User
#     queryset = User.objects.all()
#     source = ''
#
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         if not isinstance(data, list):
#             data = [data]
#         serializer = self.get_serializer(data=data, many=True)
#         serializer.is_valid(raise_exception=True)
#         added = self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response({'added_users': added}, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         return DBIUser.update_users(serializer.data, source=self.source)
#         # serializer.save()
#
#     def get(self, request, *args, **kwargs):
#         source = kwargs.get('source', '')
#         return self.list(request, many=True, source=source)
#
#     def post(self, request, *args, **kwargs):
#         self.source = kwargs.get('source', '')
#         return self.create(request, many=True)


class GetGroupsViewSet(ListModelMixin, GenericAPIView):
    serializer_class = GroupSerializerModel
    queryset = DBIGroup.model.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        groups = serializer.data
        data = [[group.get('group_id'), group.get('name')] for group in groups]
        return Response(status=status.HTTP_200_OK, data=data)

    def get(self, request):
        return self.list(request)


class SetGroupsViewSet(ListCreateAPIView):
    serializer_class = GroupSerializerModel
    queryset = DBIGroup.model.objects

    def create(self, request, *args, **kwargs):
        data = request.data
        if not isinstance(data, list):
            data = [data]
        serializer = self.get_serializer(data=data, many=True)
        serializer.is_valid(raise_exception=True)
        added = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'added_users': added}, status=status.HTTP_201_CREATED, headers=headers)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     groups = serializer.data
    #     data = [[group.get('group_id'), group.get('name')] for group in groups]
    #     return Response(status=status.HTTP_200_OK, data=data)
    #
    # def post(self, request, *args, **kwargs):
    #     return self.list(request)

# class UpdateUsersViewSet(ListModelMixin, CreateModelMixin, GenericAPIView):
#     serializer_class = UpdateUserSerializerModel
#     model = User
#     queryset = User.objects.all()
#     source = ''
#
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         if not isinstance(data, list):
#             data = [data]
#         serializer = self.get_serializer(data=data, many=True)
#         serializer.is_valid(raise_exception=True)
#         added = self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response({'added_users': added}, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         return DBIUser.update_users(serializer.data, source=self.source)
#         # serializer.save()
#
#     def get(self, request, *args, **kwargs):
#         source = kwargs.get('source', '')
#         return self.list(request, many=True, source=source)
#
#     def post(self, request, *args, **kwargs):
#         self.source = kwargs.get('source', '')
#         return self.create(request, many=True)
