from urllib.request import urlopen

from django.http import request
from social_core.exceptions import AuthForbidden
from django.core.files import File
import requests
from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, users_avatar_names=None, *args, **kwargs):
    print(response)
    if backend.name == "google-oauth2":
        print(response.keys())
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE

        if 'tagline' in response.keys():
            user.shopuserprofile.tagline = response['tagline']

        if 'aboutMe' in response.keys():
            user.shopuserprofile.aboutMe = response['aboutMe']

        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')

        if 'picture' in response.keys():
            user_avatar_url=response['picture']
            retrieved_avatar = requests.get(user_avatar_url)
            with open('user_avatar' + '.jpg', 'wb+') as f:
                f.write(retrieved_avatar.content)
            reopen = open('user_avatar' + '.jpg', 'rb')
            django_file = File(reopen)
            user.avatar.save(response['email'] + '.jpg', django_file, save=True)

        user.save()


