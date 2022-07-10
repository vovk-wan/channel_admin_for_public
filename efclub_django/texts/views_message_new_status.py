from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin

from django.http.response import Http404

from texts.models import User, UserStatus, Group, GetcourseGroup, MessageNewStatus
from texts.serializers import (
    MessageNewStatusSerializerModel,
)
from texts.services.getcourse_group import DBIGetcourseGroup
from texts.services.message_new_status import DBIMessageNewStatus

from django.conf import settings


class GetMessageForNewStatusViewSet(RetrieveModelMixin, GenericAPIView):
    serializer_class = MessageNewStatusSerializerModel
    queryset = DBIMessageNewStatus.model.objects

    def get_object(self):
        instance = self.queryset.first()
        if instance:
            return instance
        raise Http404

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
