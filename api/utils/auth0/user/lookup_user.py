from django.conf import settings

from api.users.models import User
from .create_from_token import create_from_token

import requests

"""
{
    'iss': 'https://dev-XXXXXXX.us.auth0.com/',
    'sub': 'google-oauth2|111111111111111111',
    'aud': [
        'https://dev-XXXXXXX.us.auth0.com/api/v2/',
        'https://dev-XXXXXXX.us.auth0.com/userinfo'
    ],
    'iat': 1654990327,
    'exp': 1655076727,
    'azp': 'XXXXXXXXXXXXXXXXXXXXX',
    'scope': 'openid profile email read:current_user'
}
"""

def lookup_user(key:str, token:dict):
    sub = token['sub'].split('|')[1]
    user_queryset = User.objects.filter(auth0_id=sub)
    if user_queryset:
        return user_queryset.first()
    return create_from_token(key, token)
