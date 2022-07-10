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


class ChallengerSerializerModel(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = [
            'phone',
            'telegram_id',
        ]


class GotInvitedSerializerModel(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = [
            'got_invite',
        ]


class SetGroupIdSerializerModel(serializers.Serializer):
    group_id = serializers.CharField(max_length=200)


class SetChannelsSerializerModel(serializers.Serializer):
    channel_id = serializers.IntegerField()
    channel_name = serializers.CharField(max_length=200)
    club_name = serializers.CharField(max_length=200)


class GetChannelsSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['name', 'channel_id']


class DeleteChannelsSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ('channel_id',)


class UpdateUserSerializerModel(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = [
            'phone',
            'getcourse_id',
        ]


class GetUserSerializerModel(serializers.ModelSerializer):
    date_joining_club = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = User
        fields = [
            'phone',
            'status',
            'getcourse_id',
            'got_invite',
            'date_joining_club',
        ]


class TelegramIDSerializerModel(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('telegram_id',)


class MailingSerializerModel(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('telegram_id', 'got_invite', 'status')


class GroupSerializerModel(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('group_id', 'name')


class MessageNewStatusSerializerModel(serializers.ModelSerializer):

    class Meta:
        model = MessageNewStatus
        fields = '__all__'
#
#
# class UserStatusSerializerModel(serializers.ModelSerializer):
#     class Meta:
#         model = UserStatus
#         fields = ['name', 'author', 'isbn', 'release_date', 'number_pages']
