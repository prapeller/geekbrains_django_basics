from django.test import TestCase
from django.test.client import Client

from users.models import User

SUCCESS_STATUS_CODE = 200
REDIRECT_STATUS_CODE = 302


class TestMainSmokeTest(TestCase):
    username = 'test_superuser'
    email = 'test@email.com'
    password = 'test_pass'

    new_user_data = {
        'username': 'test_username',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
        'password1': 'test_pass',
        'password2': 'test_pass',
    }

    def setUp(self) -> None:
        """preinstall User instance with is_superuser = True"""
        self.user = User.objects.create_superuser(username=self.username, email=self.email,
                                                  password=self.password)
        self.client = Client()

    def test_login(self):
        """
        testing user login
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, SUCCESS_STATUS_CODE)
        self.assertTrue(resp.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)
        resp = self.client.get('/users/login/')
        self.assertEqual(resp.status_code, REDIRECT_STATUS_CODE)