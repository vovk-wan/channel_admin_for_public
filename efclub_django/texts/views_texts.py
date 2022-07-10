from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import views

from texts.services.text import DBIText


class GetStartTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_start_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetAboutTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_about_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetPricesTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_prices_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetReviewsTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_reviews_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetMailingTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_for_mailing_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetWithInviteTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_for_invite_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetWithContactTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_want_for_get_phone_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetWantChallengeTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_want_for_challenger_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetWantClubTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_want_for_waiting_list_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetWantClubForExcludedTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_want_for_excluded_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetWantClubForEnteredTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_want_for_entered_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetWantClubForWaitingListTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_want_for_waiting_list_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetWantClubForGotLinkTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_want_for_entered_got_link_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetLinkWaitingListTextViewSet(views.APIView):
    def get(self, request):
        result = DBIText.get_link_waiting_list_text()
        return Response(status=status.HTTP_200_OK, data={'text': result})


class GetLinkToPayTextViewSet(views.APIView):
    """Возвращает ссылку на оплату"""
    def get(self, request):
        result = DBIText.get_link_to_pay()
        return Response(status=status.HTTP_200_OK, data={'text': result})
