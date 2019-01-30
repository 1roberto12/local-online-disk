from rest_framework import serializers
from .models import FileInfo, SharedFile


class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileInfo
        fields = ('name', 'path', 'is_dir', 'owner', 'size', 'creation_date')


class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ('id', 'filename', 'is_dir', 'size', 'creation_date', 'path', 'owner', 'is_public', 'shared_with')
        read_only_fields = ('id', 'owner', 'filename', 'is_dir', 'size', 'creation_date')
        # extra_kwargs = {'path': {'write_only': True}}
