from rest_framework import serializers
from friendship.models import FriendshipRequest
from django.apps import apps as django_apps
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = ('id', 'email', 'username',)

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendshipRequest
        fields = ('to_user', 'from_user', 'created')


class DownloadStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = django_apps.get_model('api', 'DownloadStatistic')
        fields = ('filename', 'path', 'day', 'count')
