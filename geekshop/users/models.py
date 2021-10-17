from datetime import timedelta, datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

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


class UserProfile(models.Model):
    CHOICES = [('m', 'Male'), ('f', 'Female')]
    user = models.OneToOneField(User, unique=True, null=False, db_index=True,
                                on_delete=models.CASCADE)

    tagline = models.CharField(verbose_name='tags', max_length=128, blank=True)
    about = models.TextField(verbose_name='about me', max_length=512, blank=True,
                             null=True, )
    gender = models.CharField(verbose_name='gender',
                              choices=CHOICES,
                              max_length=1, blank=True, )
