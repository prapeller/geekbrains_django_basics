from django.test import TestCase
from django.test.client import Client

from users.models import User
from users.views import Register, send_verify_link

STATUS_CODE_SUCCESS = 200
STATUS_CODE_REDIRECT = 302


class TestMainSmokeTest(TestCase):
    username = 'test_superuser'
    email = 'test_superuser@email.com'
    password = 'test_pass'

    new_user_data = {
        'username': 'test_user',
        'email': 'test_user@email.com',
        'first_name': 'test_first',
        'last_name': 'test_last',
        'age': '18',
        'password1': '123Test_pass!',
        'password2': '123Test_pass!',
    }

    def setUp(self) -> None:
        """preinstall User instance with is_superuser = True"""
        self.user = User.objects.create_superuser(username=self.username, email=self.email,
                                                  password=self.password)
        self.client = Client()

    def test_login(self):
        """
        test that
        logged out user is anonymous
        logged in superuser is redirected to main when trying to visit 'users/login/'
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, STATUS_CODE_SUCCESS)
        self.assertTrue(resp.context['user'].is_anonymous)

        self.client.login(username=self.username, password=self.password)
        resp = self.client.get('/users/login/')
        self.assertEqual(resp.status_code, STATUS_CODE_REDIRECT)

    def test_register(self):
        """test new registered user is redirected to login
        register and varify new_user
        """
        resp = self.client.post('/users/register/', data=self.new_user_data)
        self.assertEqual(resp.status_code, STATUS_CODE_REDIRECT)
        all_users = User.objects.all()
        new_user = User.objects.get(username=self.new_user_data['username'])
        activation_link = send_verify_link(new_user)
        print(activation_link)

        resp = self.client.get(activation_link)
        self.assertEqual(resp.status_code, STATUS_CODE_SUCCESS)

        new_user.refresh_from_db()
        self.assertTrue(new_user.is_active)

    def tearDown(self) -> None:
        pass

