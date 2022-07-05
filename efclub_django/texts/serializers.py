from rest_framework import serializers
from texts.models import (
    User, UserStatus, MessageNewStatus, Text, Group, GetcourseGroup, Channel
)


class UserSerializerModel(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = [
            'phone',
            'status',
            'status_updated',
            'got_invite',
            'expiration_date',
            'date_joining_club',
        ]


class SetGroupIdSerializerModel(serializers.Serializer):
    group_id = serializers.CharField(max_length=200)


class UpdateUserSerializerModel(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = [
            'phone',
            'getcourse_id',
        ]


class TelegramIDSerializerModel(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('telegram_id',)


class MailingSerializerModel(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('telegram_id', 'got_invite', 'status')


class UserStatusSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = UserStatus
        fields = ['name', 'author', 'isbn', 'release_date', 'number_pages']
