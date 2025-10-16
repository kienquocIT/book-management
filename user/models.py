import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(null=True, upload_to='avatars/')

    def __str__(self):
        return self.username

class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
