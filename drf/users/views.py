from django.db import IntegrityError
from friendship.models import Friend, Follow, Block
from rest_framework import status, generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import models
from . import serializers
from django.contrib.auth import get_user_model


class UserListView(generics.ListCreateAPIView):
    queryset = models.CustomUser.objects.all()
    serializer_class = serializers.UserSerializer


class FriendshipView(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.FriendRequestSerializer
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
        r.accept()
        return Response({'status': 'Request sent'}, status=201)

    def friendsList(self, request, *args, **kwargs):
        self.serializer_class = serializers.UserSerializer
        self.queryset = Friend.objects.friends(request.user)
        return super().list(request, *args, **kwargs)

    def removeFriend(self, request):
        User = get_user_model()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        other_user = User.objects.get(pk=request.data.get('to_user'))
        Friend.objects.remove_friend(request.user, other_user)
        return Response({'status': 'Friend removed'}, status=201)

    def sentRequestList(self, request, *args, **kwargs):
        self.queryset = Friend.objects.sent_requests(user=request.user)
        return   super().list(request, *args, **kwargs)
