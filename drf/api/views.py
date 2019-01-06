from django.http import FileResponse
from rest_framework import status, generics, viewsets, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django.conf import settings
from django.shortcuts import redirect
from .serializers import FileInfoSerializer
from .services import FileStorageService


class FileList(generics.ListAPIView):
    serializer_class = FileInfoSerializer
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, p=None, *args, **kwargs):
        self.queryset = FileStorageService.get_files(p)
        return self.list(request, *args, **kwargs)


class FileInfoViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = FileStorageService.get_files()
    serializer_class = FileInfoSerializer
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def check_user_folder(request) -> None:
        username = request.user.username
        files = FileStorageService.get_files()
        directories = filter(lambda entry: entry.is_dir, files)
        if username not in [directory.name for directory in directories]:
            FileStorageService.create_directory(username)

    def list(self, request, p=None, *args, **kwargs):
        self.check_user_folder(request)
        self.queryset = FileStorageService.get_files(p, user=request.user.username)
        return super().list(request, *args, **kwargs)

    def download(self, request, p=None, *args, **kwargs):
        self.check_user_folder(request)
        obj = FileStorageService.get_filestream(p, user=request.user.username)
        response = FileResponse(obj)
        response['Content-Disposition'] = f'attachment; filename= "{FileStorageService.get_filename(p, user=request.user.username)}"'
        return response

    def create(self, request: Request, p=None, *args, **kwargs):
        self.check_user_folder(request)
        FileStorageService.save_file(p, request.FILES['f'].name, request.FILES['f'].file, user=request.user.username)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, p=None, *args, **kwargs):
        self.check_user_folder(request)
        FileStorageService.remove(p, user=request.user.username)
        return Response(status=status.HTTP_204_NO_CONTENT)
