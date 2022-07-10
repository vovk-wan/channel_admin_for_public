from django.urls import path

from texts.views_getcourse_group import (
    GetGroupViewSet,
    SetGroupViewSet
)

urlpatterns = [
    path('getcourse_group/get/', GetGroupViewSet.as_view(), name='get_group'),
    path('getcourse_group/set/<str:group_name>', SetGroupViewSet.as_view(), name='set_group'),
]

