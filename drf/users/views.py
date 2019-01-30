from django.db import IntegrityError
from django.apps import apps as django_apps
from friendship.models import Friend, Follow, Block
from rest_framework import status, generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from django.contrib.auth import get_user_model
from friendship.models import FriendshipRequest


class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer

class FriendshipViewTo(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.ToRequestSerializer
    permission_classes = (IsAuthenticated,)

    def sendRequest(self, request):
        User = get_user_model()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        other_user = User.objects.get(pk=request.data.get('to_user'))
        try:
            r = Friend.objects.add_friend(
                request.user,
                other_user,
                message='Hi! I would like to add you')
        except IntegrityError:
            return Response({'status': 'Friendship already requested'}, status=201)
        return Response({'status': 'Request sent'}, status=201)

    def sentRequestList(self, request, *args, **kwargs):
        self.queryset = Friend.objects.sent_requests(user=request.user)
        return   super().list(request, *args, **kwargs)

class FriendshipViewFrom(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.FromRequestSerializer
    permission_classes = (IsAuthenticated,)

    def friendsList(self, request, *args, **kwargs):
        self.serializer_class = serializers.UserSerializer
        self.queryset = Friend.objects.friends(request.user)
        return super().list(request, *args, **kwargs)

    def removeFriend(self, request):
        User = get_user_model()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        other_user = User.objects.get(pk=request.data.get('from_user'))
        Friend.objects.remove_friend(request.user, other_user)
        return Response({'status': 'Friend removed'}, status=201)

    def unreadRequestList(self, request, *args, **kwargs):
        self.queryset = Friend.objects.unread_requests(user=request.user)
        return   super().list(request, *args, **kwargs)

    def unrejectedRequestList(self, request, *args, **kwargs):
        self.queryset = Friend.objects.unrejected_requests(user=request.user)
        return super().list(request, *args, **kwargs)

    def rejectedRequestList(self, request, *args, **kwargs):
        self.queryset = Friend.objects.rejected_requests(user=request.user)
        return super().list(request, *args, **kwargs)

    def acceptRequest(self, request):
        friend_request = FriendshipRequest.objects.get(from_user=request.data.get('from_user'))
        friend_request.accept()
        return Response({'status': 'Request accepted'}, status=201)

    def rejectRequest(self, request):
        friend_request = FriendshipRequest.objects.get(from_user=request.data.get('from_user'))
        friend_request.reject()
        return Response({'status': 'Request rejected'}, status=201)


class StatisticsView(generics.ListAPIView):
    serializer_class = serializers.DownloadStatisticSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        DownloadStatistic = django_apps.get_model('api', 'DownloadStatistic')
        queryset = DownloadStatistic.objects.filter(user=self.request.user)
        file = self.request.query_params.get('dir', None)
        if file is not None:
            queryset = filter(lambda stat: '/' not in stat.path[len(file):], queryset.filter(path=file))
        else:
            queryset = queryset.exclude(path__regex=r'/.+')
        return queryset
