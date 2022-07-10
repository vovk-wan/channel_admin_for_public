from django.urls import path

from texts.views_texts import (
    GetStartTextViewSet,
    GetAboutTextViewSet,
    GetPricesTextViewSet,
    GetReviewsTextViewSet,
    GetMailingTextViewSet,
    GetWithInviteTextViewSet,
    GetWithContactTextViewSet,
    GetWantChallengeTextViewSet,
    GetWantClubTextViewSet,
    GetWantClubForExcludedTextViewSet,
    GetWantClubForEnteredTextViewSet,
    GetWantClubForGotLinkTextViewSet,
    GetLinkWaitingListTextViewSet,
    GetLinkToPayTextViewSet,
    GetWantClubForWaitingListTextViewSet,

)

urlpatterns = [
    path('text/start/', GetStartTextViewSet.as_view(), name='start_text'),
    path('text/about/', GetAboutTextViewSet.as_view(), name='about_text'),
    path('text/prices/', GetPricesTextViewSet.as_view(), name='prices_text'),
    path('text/reviews/', GetReviewsTextViewSet.as_view(), name='reviews_text'),
    path('text/mailing/', GetMailingTextViewSet.as_view(), name='mailing_text'),
    path('text/invite/', GetWithInviteTextViewSet.as_view(), name='invite_text'),
    path('text/contact/', GetWithContactTextViewSet.as_view(), name='contact_text'),
    path('text/want_club_challenger/', GetWantChallengeTextViewSet.as_view(), name='want_club_challenger_text'),
    path('text/want_club/', GetWantClubTextViewSet.as_view(), name='want_club_text'),
    path('text/want_club_for_excluded/', GetWantClubForExcludedTextViewSet.as_view(), name='want_club_for_excluded_text'),
    path('text/want_club_for_entered/', GetWantClubForEnteredTextViewSet.as_view(), name='want_club_for_entered_text'),
    path('text/want_club_for_waiting_list/', GetWantClubForWaitingListTextViewSet.as_view(), name='want_club_for_waithing_text'),
    path('text/want_club_for_got_link/', GetWantClubForGotLinkTextViewSet.as_view(), name='want_club_for_got_link_text'),
    path('text/waiting_list_link/', GetLinkWaitingListTextViewSet.as_view(), name='waiting_list_link_text'),
    path('text/pay_link/', GetLinkToPayTextViewSet.as_view(), name='waiting_list_link_text'),
]
