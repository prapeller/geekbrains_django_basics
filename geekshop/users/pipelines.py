import os.path
import urllib.request
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode
from PIL import Image
from io import BytesIO

import requests

from django.utils import timezone
from django.core.files import File
from social_core.exceptions import AuthException, AuthForbidden
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
             OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'lang', 'photo')),
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

    languages = {
        '0': 'Russian',
        '1': 'Ukrainian',
        '2': 'Belorussian',
        '3': 'English',
    }
    if data.get('language'):
        language_code = data.get('language')
        user.userprofile.lang = languages.get(language_code)

    if data.get('photo'):
        vk_photo_url = data.get('photo')

        res = requests.get(vk_photo_url)
        img = Image.open(BytesIO(res.content))

        ext = vk_photo_url.split('?size')[-2].split('.')[-1]
        image_url = f'users_image/{user.username}.{ext}'
        user.image.name = image_url

        temp_image = open(f'media/{image_url}', 'w')
        img.save(temp_image, 'JPEG')


    if data.get('bdate'):
        bdate_data = data.get('bdate')
        bdate_timestamp = datetime.strptime(bdate_data, '%d.%m.%Y')
        bdate = bdate_timestamp.date()
        age = timezone.now().date().year - bdate.year
        user.age = age
        if age < 18:
            user.delete()
            # raise AuthException('social_core.backends.vk.VKOAuth2')
            # respond 'server 500 error'
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.save()
