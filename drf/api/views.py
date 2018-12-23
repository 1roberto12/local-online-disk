from django.http import FileResponse
from rest_framework import status, generics, viewsets, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import redirect
from .serializers import FileInfoSerializer
from .services import get_files, get_filestream, get_filename, save_file


class FileList(generics.ListAPIView):
    serializer_class = FileInfoSerializer
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, p=None, *args, **kwargs):
        # if not request.user.is_authenticated:
        #    return redirect('/api/v1/rest-auth/login')
        self.queryset = get_files(p or '/')
        return self.list(request, *args, **kwargs)


class FileInfoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = get_files('/')
    serializer_class = FileInfoSerializer
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def list(self, request, p=None, *args, **kwargs):
        self.queryset = get_files(p or '/')
        return super().list(request, *args, **kwargs)

    @staticmethod
    def download(request, p=None, *args, **kwargs):
        obj = get_filestream(p)
        response = FileResponse(obj)
        response['Content-Disposition'] = f'attachment; filename= "{get_filename(p)}"'
        return response

    def create(self, request: Request, p=None, *args, **kwargs):
        save_file(p or '/', request.FILES['f'])
        return Response(status=status.HTTP_200_OK)
