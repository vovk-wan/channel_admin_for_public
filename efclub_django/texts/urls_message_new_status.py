from django.urls import path

from texts.views_message_new_status import (
    GetMessageForNewStatusViewSet,
)

urlpatterns = [
    path('message_new_status/', GetMessageForNewStatusViewSet.as_view(), name='update_users'),
]
