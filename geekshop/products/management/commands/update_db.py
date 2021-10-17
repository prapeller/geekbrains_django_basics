from django.core.management.base import BaseCommand
from django.db import connection

from os import path
from users.models import User, UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            UserProfile.objects.create(user=user)

