from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.shortcuts import redirect
from .serializers import FileInfoSerializer
from .services import get_files


class FileList(generics.ListAPIView):
    serializer_class = FileInfoSerializer
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, p=None, *args, **kwargs):
        # if not request.user.is_authenticated:
        #    return redirect('/api/v1/rest-auth/login')
        self.queryset = get_files(p or '/')
        return self.list(request, *args, **kwargs)
