# -*- coding: utf-8 -*-
import redis
import memcache

import unittest

from alf.managers import Token
from alf.tokens import TokenStorage


class TestToken(unittest.TestCase):

    def setUp(self):
        self.storage_obj = None

    def test_should_have_an_access_token(self):
        token = Token(access_token='access_token',
                      storage_object=self.storage_obj)
        self.assertEqual(token.access_token, 'access_token', self.storage_obj)

    def test_should_know_when_it_has_expired(self):
        token = Token(access_token='access_token',
                      expires_in=0,
                      storage_object=self.storage_obj)
        self.assertFalse(token.is_valid(), self.storage_obj)

    def test_should_know_when_it_is_valid(self):
        token = Token(access_token='access_token',
                      expires_in=10,
                      storage_object=self.storage_obj)
        self.assertTrue(token.is_valid(), self.storage_obj)


class TestTokenStorage(TestToken):

    def setUp(self):
        self.storage_obj = TokenStorage()


class TestTokenRedis(TestToken):

    def setUp(self):
        self.storage_obj = redis.StrictRedis(host='localhost', port=6379, db=0)
        try:
            self.storage_obj.scan()
        except redis.ConnectionError:
            self.skipTest("You don't have a Redis server")

    def tearDown(self):
        self.storage_obj.delete('access_token')


class TestTokenMemcached(TestToken):

    def setUp(self):
        self.storage_obj = memcache.Client(['127.0.0.1:11211'], debug=1)
        if not self.storage_obj.get_stats():
            self.skipTest("You don't have a Memcached server")

    def tearDown(self):
        self.storage_obj.delete('access_token')

