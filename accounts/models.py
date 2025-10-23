from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    full_name = models.CharField(max_length=255)

    username = models.CharField(max_length=15, unique=True)

    email = models.EmailField(unique=True)

    course = models.CharField(blank=True, null=True, max_length=15)

    is_blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.username