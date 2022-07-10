from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import views, GenericAPIView, ListAPIView, CreateAPIView, DestroyAPIView

from texts.serializers import GetChannelsSerializerModel, DeleteChannelsSerializerModel
from texts.services.channel import DBIChannel


class GetChannelsViewSet(ListAPIView, GenericAPIView):
    serializer_class = GetChannelsSerializerModel
    queryset = DBIChannel.get_channels()

    def get(self, request, *args, **kwargs):
        return self.list(request)


class AddChannelViewSet(CreateAPIView, GenericAPIView):
    serializer_class = GetChannelsSerializerModel

    def perform_create(self, serializer):
        DBIChannel.add_channel(**serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request)


class DeleteChannelsViewSet(DestroyAPIView):
    serializer_class = DeleteChannelsSerializerModel
    queryset = DBIChannel.model.objects

    def get_object(self):
        data = self.request.data
        instance = self.queryset.filter(**data).first()
        if not instance:
            raise Http404
        return instance

    def post(self, reuest, *args, **kwargs):
        return self.delete(reuest, *args, **kwargs)
