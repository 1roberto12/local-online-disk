from datetime import date

from django.http import FileResponse
from rest_framework import status, generics, viewsets, mixins
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.conf import settings
from django.shortcuts import redirect

from .permissions import IsPublicOrSharedWithMe
from .models import SharedFile, FileInfo, DownloadStatistic
from .serializers import FileInfoSerializer, SharedFileSerializer
from .services import FileStorageService


class FileInfoView(generics.ListCreateAPIView, generics.DestroyAPIView, generics.GenericAPIView):
    queryset = FileStorageService.get_files()
    serializer_class = FileInfoSerializer
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'p'

    @staticmethod
    def check_user_folder(request) -> None:
        username = request.user.username
        files = FileStorageService.get_files()
        directories = filter(lambda entry: entry.is_dir, files)
        if username not in [directory.name for directory in directories]:
            FileStorageService.create_directory(username)

    def get(self, request, p=None, *args, **kwargs):
        self.check_user_folder(request)
        entry = FileStorageService.get_dir_entry(p, user=request.user.username)
        if entry.is_dir:
            self.queryset = FileStorageService.get_files(p, user=request.user.username)
            for f in self.queryset:
                path = f.path[:-len(f.name) - 1]
                path = '/' if path == '' else path
                DownloadStatistic.objects.get_or_create(filename=f.name, path=path, user=request.user,
                                                        defaults={'count': -1 if f.is_dir else 0})
            return super().list(request, *args, **kwargs)
        else:
            return self.download(request, p, *args, **kwargs)

    def download(self, request, p=None, *args, **kwargs):
        self.check_user_folder(request)
        obj = FileStorageService.get_filestream(p, user=request.user.username)
        filename = FileStorageService.get_filename(p, user=request.user.username)
        stat = DownloadStatistic.objects.filter(path=p, filename=filename, user=request.user, day=date.today())
        if len(stat) == 1:
            stat.update(count=stat[0].count + 1)
        else:
            DownloadStatistic.objects.create(path=p, filename=filename, user=request.user, count=1)
        response = FileResponse(obj)
        response['Content-Disposition'] = f'attachment; filename= "{filename}"'
        return response

    def post(self, request, p=None, *args, **kwargs):
        self.check_user_folder(request)
        if 'f' in request.FILES:
            FileStorageService.save_file(p, request.FILES['f'].name, request.FILES['f'].file,
                                         user=request.user.username)
            DownloadStatistic.objects.create(path=(p or '/'), filename=request.FILES['f'].name, user=request.user)
        else:
            try:
                FileStorageService.get_dir_entry(p, user=request.user.username)
            except ValidationError:
                FileStorageService.create_directory(p, user=request.user.username)
            else:
                raise ValidationError('Directory already exists')
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, p=None, *args, **kwargs):
        self.check_user_folder(request)
        FileStorageService.remove(p, user=request.user.username)
        filename = p[p.rfind('/') + 1:]
        path = p[:-len(filename) - 1]
        path = '/' if path == '' else path
        DownloadStatistic.objects.filter(path=path, filename=filename, user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FileSharingView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer
    lookup_field = 'id'
    permission_classes = (IsPublicOrSharedWithMe,)

    def retrieve(self, request, p=None, *args, **kwargs):
        instance: SharedFile = self.get_object()
        entry = FileStorageService.get_dir_entry(instance.path, instance.owner.username)
        if entry.is_dir:
            self.serializer_class = FileInfoSerializer
            if p is not None:
                entry = FileStorageService.get_dir_entry(instance.path + '/' + p, user=instance.owner.username)
                if entry.is_dir:
                    self.queryset = list(
                        map(lambda f: FileInfo(name=f.name, path='/' + p + '/' + f.name, is_dir=f.is_dir, size=f.size,
                                               owner=f.owner, creation_date=f.creation_date),
                            FileStorageService.get_files(instance.path + '/' + p, user=instance.owner.username)))
                else:
                    obj = FileStorageService.get_filestream(instance.path + '/' + p, user=instance.owner.username)
                    response = FileResponse(obj)
                    response['Content-Disposition'] = f'attachment; filename= "{entry.name}"'
                    return response
            else:
                self.queryset = list(
                    map(lambda f: FileInfo(name=f.name, path='/' + f.name, is_dir=f.is_dir, size=f.size, owner=f.owner,
                                           creation_date=f.creation_date),
                        FileStorageService.get_files(instance.path, user=instance.owner.username)))
            return super().list(request, *args, **kwargs)
        else:
            if p is not None:
                raise ValidationError('Invalid path')
            else:
                obj = FileStorageService.get_filestream(instance.path, user=instance.owner.username)
            response = FileResponse(obj)
            response['Content-Disposition'] = f'attachment; filename= "{entry.name}"'
            return response

    def get(self, request, *args, **kwargs):
        if 'id' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            if not request.user.is_authenticated:
                raise PermissionDenied()
            if request._request.path.endswith('my/'):
                self.queryset = SharedFile.objects.filter(owner=request.user.id)
            else:
                self.queryset = SharedFile.objects.filter(shared_with=request.user.id)
            return super().list(request, *args, **kwargs)

    def perform_create(self, serializer: SharedFileSerializer):
        try:
            entry = FileStorageService.get_dir_entry(serializer.validated_data['path'], user=self.request.user.username)
        except ValidationError:
            raise

        serializer.save(owner=self.request.user, filename=entry.name, is_dir=entry.is_dir, size=entry.size,
                        creation_date=entry.creation_date)


class EncryptionView(generics.GenericAPIView):
    queryset = []
    permission_classes = (IsAuthenticated, )

    def post(self, request, p=None, *args, **kwargs):
        FileInfoView.check_user_folder(request)
        entry = FileStorageService.get_dir_entry(p, user=request.user.username)
        if entry.is_dir:
            raise ValidationError('Cannot encrypt directory')
        if 'password' not in request.data:
            raise ValidationError({'password': ['This field is required.']})
        if 'decrypt' not in request.data:
            FileStorageService.encrypt(entry, request.data['password'])
        else:
            FileStorageService.decrypt(entry, request.data['password'])
        return Response(status=status.HTTP_200_OK)
