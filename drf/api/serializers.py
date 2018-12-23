from rest_framework import serializers
from .models import FileInfo


class FileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileInfo
        fields = ('name', 'path', 'is_dir', 'owner', 'size', 'creation_date')
