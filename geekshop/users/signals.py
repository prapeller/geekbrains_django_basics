from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile


@receiver(signal=post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(signal=post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
