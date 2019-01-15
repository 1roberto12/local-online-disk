from rest_framework import serializers
from .models import FileInfo, SharedFile


class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileInfo
        fields = ('name', 'path', 'is_dir', 'owner', 'size', 'creation_date')


class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ('id', 'path', 'owner', 'is_public', 'shared_with')
        read_only_fields = ('id', 'owner', 'filename')
        # extra_kwargs = {'path': {'write_only': True}}
