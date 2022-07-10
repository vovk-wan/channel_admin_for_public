from django.urls import path

from texts.views_group import (
    GetGroupsViewSet,
    SetGroupsViewSet,

)

urlpatterns = [
    path('groups/get/', GetGroupsViewSet.as_view(), name='get_groups'),
    path('groups/set/', SetGroupsViewSet.as_view(), name='set_groups'),
]
