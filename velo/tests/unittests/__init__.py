# -*- coding: utf-8 -*-
from unittest import TestCase

from pyramid.decorator import reify
from pyramid import testing


class TestBase(TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('velo.model')

    @reify
    def db(self):
        from velo.model.meta import IMongoConnection, DATABASE_NAME
        conn = self.config.registry.getUtility(IMongoConnection)
        return getattr(conn, DATABASE_NAME)

    def get_request(self):
        request = testing.DummyRequest()
        request.db = self.db
        return request
