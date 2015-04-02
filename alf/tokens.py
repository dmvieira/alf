# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

TOKEN_KEY = 'access_token'
TOKEN_VALUE = ''

class TokenError(Exception):

    def __init__(self, message, response):
        super(TokenError, self).__init__(message)
        self.response = response


class Token(object):

    def __init__(self, access_token='', expires_in=0, storage_object=None):
        self._storage_object = storage_object or TokenStorage()
        self.access_token = access_token
        self._expires_in = expires_in

        self._expires_on = datetime.now() + timedelta(seconds=self._expires_in)

    def is_valid(self):
        return self._expires_on > datetime.now()

    @property
    def access_token(self):
        self._access_token = self._storage_object.get(TOKEN_KEY)
        return self._access_token

    @access_token.setter
    def access_token(self, token):
        self._access_token = token
        self._storage_object.set(TOKEN_KEY, self._access_token)


class TokenStorage(object):

    def __init__(self, key=TOKEN_KEY, token=TOKEN_VALUE):
        self.storage = dict()
        self.set(key, token)

    def get(self, key=TOKEN_KEY):
        return self.storage.get(key)

    def set(self, key=TOKEN_KEY, token=TOKEN_VALUE):
        self.storage[key] = token

