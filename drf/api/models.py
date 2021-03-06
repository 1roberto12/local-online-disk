import uuid
from django.db import models


class FileInfo(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    is_dir = models.BooleanField()
    size = models.PositiveIntegerField()
    owner = models.CharField(max_length=100)
    creation_date = models.DateTimeField()

    def save(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass


class SharedFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    filename = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    is_dir = models.BooleanField()
    creation_date = models.DateTimeField()
    size = models.PositiveIntegerField()
    owner = models.ForeignKey('users.CustomUser', related_name='shared_files', on_delete=models.CASCADE)
    is_public = models.BooleanField()
    shared_with = models.ManyToManyField('users.CustomUser', blank=True)

    class Meta:
        ordering = ('filename',)


class DownloadStatistic(models.Model):
    filename = models.CharField(max_length=100)
    path = models.CharField(max_length=512, default='/')
    user = models.ForeignKey('users.CustomUser', related_name='owner', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    day = models.DateField(auto_now_add=True)

