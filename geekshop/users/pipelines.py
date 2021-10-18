from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests

from django.utils import timezone
from social_core.exceptions import AuthException
from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(
        ('http',
         'api.vk.com',
         '/method/users.get',
         None,
         urlencode(
            OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                        access_token=response['access_token'],
                        v=5.131)),
         None
         )
    )

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]

    if data.get('sex'):
        user.userprofile.gender = 'f' if data.get('sex') == 1 else 'm'

    if data.get('about'):
        user.userprofile.about = data.get('about')

    if data.get('bdate'):
        bdate_data = data.get('bdate')
        bdate_timestamp = datetime.strptime(bdate_data, '%d.%m.%Y')
        bdate = bdate_timestamp.date()
        age = timezone.now().date().year - bdate.year
        user.age = age
        if age > 18:
            user.delete()
            raise AuthException('social_core.backends.vk.VKOAuth2')
        user.save()
