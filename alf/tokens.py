# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

TOKEN_KEY = 'access_token'
TOKEN_VALUE = ''
TOKEN_EXPIRES = 'token_expires_on'

class TokenError(Exception):

    def __init__(self, message, response):
        super(TokenError, self).__init__(message)
        self.response = response


class Token(object):

    def __init__(self, access_token='', expires_in=0):
        self.access_token = access_token
        self._expires_in = expires_in

        self.expires_on = datetime.now() + timedelta(seconds=self._expires_in)

    def is_valid(self):
        return self.expires_on > datetime.now()


class TokenStorage(object):
    def __init__(self, custom_storage=None):
        self._storage = custom_storage or TokenDefaultStorage()
        self._access_token = TOKEN_VALUE
        self._expires_on = None
    
    def __call__(self, token):
        self._storage.set(TOKEN_KEY, token.access_token)
        self._storage.set(TOKEN_EXPIRES, token.expires_on
        
    @property
    def access_token(self):


class TokenDefaultStorage(object):

    def __init__(self, key=TOKEN_KEY, token=TOKEN_VALUE):
        self.storage = dict()
        self.set(key, token)

    def get(self, key=TOKEN_KEY):
        return self.storage.get(key)

    def set(self, key=TOKEN_KEY, token=TOKEN_VALUE):
        self.storage[key] = token

