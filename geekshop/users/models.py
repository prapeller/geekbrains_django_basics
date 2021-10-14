from datetime import timedelta, datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

NULL_INSTALL = {'null': True, 'blank': True}


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=True)
    image = models.ImageField(upload_to='users_image', blank=True)
    age = models.PositiveIntegerField(default=18)

    activation_key = models.CharField(max_length=128, **NULL_INSTALL)
    activation_key_created = models.DateTimeField(auto_now_add=True,
                                                  **NULL_INSTALL)

    def is_activation_key_expired(self):
        expires_on = self.activation_key_created + timedelta(hours=48)
        return True if now() > expires_on else False
