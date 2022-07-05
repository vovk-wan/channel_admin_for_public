from django.urls import path

from texts.views import (
    UpdateUsersViewSet,
    UpdateFromGetcourse,
    GetExcludeUsersViewSet,
    GetUsersForMailingNewStatusViewSet,
    GetMembersForMailingNewStatusViewSet,
    RemovesStatusUpdatedUsersViewSet,
    RemovesStatusUpdatedMembersViewSet,
    GetGroupViewSet,
    SetGroupViewSet
)

urlpatterns = [
    path('update_users/<str:source>', UpdateUsersViewSet.as_view(), name='update_users'),
    path('users/excluded', GetExcludeUsersViewSet.as_view(), name='excluded_users'),
    path('users/mailing', GetUsersForMailingNewStatusViewSet.as_view(), name='get_updated_users'),
    path('users/mailing_members', GetMembersForMailingNewStatusViewSet.as_view(), name='get_updated_members'),
    path('users/removes_status_updated_users', RemovesStatusUpdatedUsersViewSet.as_view(), name='remove_updated_users'),
    path('users/removes_status_updated_members', RemovesStatusUpdatedMembersViewSet.as_view(), name='remove_updated_members'),
    path('groups/get_group/<str:group_name>', GetGroupViewSet.as_view(), name='get_group'),
    path('groups/set_group/<str:group_name>', SetGroupViewSet.as_view(), name='set_group'),
    path('', UpdateFromGetcourse.as_view(), name='update_user')
]
