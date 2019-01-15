from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    shared_with_me = models.ManyToManyField('api.SharedFile')

    def __str__(self):
        return self.email