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
