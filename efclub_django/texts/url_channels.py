from django.urls import path

from texts.views_channels import (
    GetChannelsViewSet,
    AddChannelViewSet,
    DeleteChannelsViewSet
)

urlpatterns = [
    path('channels/get/', GetChannelsViewSet.as_view(), name='get_channels'),
    path('channels/add_channel/', AddChannelViewSet.as_view(), name='set_channel'),
    path('channels/delete/', DeleteChannelsViewSet.as_view(), name='delete_channel')
]

