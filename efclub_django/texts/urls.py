from django.urls import path

from texts.views import (
    UpdateUsersViewSet,
    GetExcludeUsersViewSet,
    GetUsersForMailingNewStatusViewSet,
    GetMembersForMailingNewStatusViewSet,
    GetUsersForWaitingListWithTelegramIdViewSet,
    RemovesStatusUpdatedUsersViewSet,
    RemovesStatusUpdatedMembersViewSet,
    GetUserByTelegramIDViewSet,
    AddChallengerViewSet,
    GotInvitedViewSet
)

urlpatterns = [
    path('update_users/<str:source>', UpdateUsersViewSet.as_view(), name='update_users'),
    path('users/excluded/', GetExcludeUsersViewSet.as_view(), name='excluded_users'),
    path('users/mailing/', GetUsersForMailingNewStatusViewSet.as_view(), name='get_updated_users'),
    path('users/mailing_members/', GetMembersForMailingNewStatusViewSet.as_view(), name='get_updated_members'),
    path('users/get_users_from_waiting_list/', GetUsersForWaitingListWithTelegramIdViewSet.as_view(), name='get_users_from_waiting_list'),
    path('users/removes_status_updated_users/', RemovesStatusUpdatedUsersViewSet.as_view(), name='remove_updated_users'),
    path('users/removes_status_updated_members/', RemovesStatusUpdatedMembersViewSet.as_view(), name='remove_updated_members'),
    path('users/get_users_by_telegram_id/<int:telegram_id>', GetUserByTelegramIDViewSet.as_view(), name='get_users_by_telegram_id'),
    path('users/add_challenger/', AddChallengerViewSet.as_view(), name='add_challenger'),
    path('users/got_invited/<int:telegram_id>', GotInvitedViewSet.as_view(), name='got_invited'),

]
