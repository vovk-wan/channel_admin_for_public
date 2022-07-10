from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import views, GenericAPIView

from texts.serializers import SetGroupIdSerializerModel
from texts.services.getcourse_group import DBIGetcourseGroup


class GetGroupViewSet(views.APIView):
    def get(self, request, *args, **kwargs):
        group_name = kwargs.get('club')
        result = DBIGetcourseGroup.get_group()
        return Response(status=status.HTTP_200_OK, data=result)


class SetGroupViewSet(GenericAPIView):
    serializer_class = SetGroupIdSerializerModel

    def post(self, request, *args, **kwargs):
        group_name = kwargs.get('group_name')
        group_id = request.data.get('group_id')
        result = DBIGetcourseGroup.set_group(group_id=group_id, group_name=group_name)
        return Response(status=status.HTTP_201_CREATED, data=result)

    def get(self, request, *args, **kwargs):
        return Response()
