from django.core.management.base import BaseCommand
from django.db import connection

from os import path
from users.models import User, UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        userprofiles = UserProfile.objects.all()
        userprofiles_users_ids = list(map(lambda profile: profile.user_id, userprofiles))
        users = User.objects.all()
        for user in users:
            if user.pk not in userprofiles_users_ids:
                UserProfile.objects.create(user=user)
