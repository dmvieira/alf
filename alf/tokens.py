# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

TOKEN_KEY = 'access_token'
TOKEN_VALUE = ''
TOKEN_EXPIRES = 'expires_on'


class TokenError(Exception):

    def __init__(self, message, response):
        super(TokenError, self).__init__(message)
        self.response = response


class Token(object):

    def __init__(self, access_token='', expires_on=0):
        self.access_token = access_token

        self.expires_on = expires_on or self.calc_expires_on()

    def is_valid(self):
        return self.expires_on > datetime.now()

    @staticmethod
    def calc_expires_on(expires_in=0):
        return datetime.now() + timedelta(seconds=int(expires_in))


class TokenStorage(object):
    def __init__(self, custom_storage=None):
        self._storage = custom_storage or TokenDefaultStorage()

    def __call__(self, token):
        self._storage.set(TOKEN_KEY, token.access_token)
        self._storage.set(TOKEN_EXPIRES, str(token.expires_on))

    def request_token(self):
        access_token = self._storage.get(TOKEN_KEY)
        expires_on = self._storage.get(TOKEN_EXPIRES)
        
        if access_token and expires_on:
            return {TOKEN_KEY: access_token,
                    TOKEN_EXPIRES: datetime.strptime(expires_on,
                                                     "%Y-%m-%d %H:%M:%S.%f")}
        return dict()

class TokenDefaultStorage(object):

    def __init__(self, key=TOKEN_KEY, token=TOKEN_VALUE):
        self.storage = dict()
        self.set(key, token)

    def get(self, key=TOKEN_KEY):
        return self.storage.get(key)

    def set(self, key=TOKEN_KEY, token=TOKEN_VALUE):
        self.storage[key] = token

