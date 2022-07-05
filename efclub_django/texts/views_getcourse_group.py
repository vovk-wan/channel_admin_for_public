from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import views

from texts.services.getcourse_group import DBIGetcourseGroup


class GetStartTextViewSet(views.APIView):
    def get(self, request):
        result = DBIGetcourseGroup.get_start_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})

