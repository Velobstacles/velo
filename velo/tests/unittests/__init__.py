# -*- coding: utf-8 -*-
from functools import partial
from unittest import TestCase

from pyramid.decorator import reify
from pyramid import testing

from pyramid_rest import rest_resource_path, rest_resource_url


class TestBase(TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_rest')
        self.config.include('velo')

    def tearDown(self):
        testing.tearDown()

    @reify
    def db(self):
        from velo.model.meta import IMongoConnection, DATABASE_NAME
        conn = self.config.registry.getUtility(IMongoConnection)
        return getattr(conn, DATABASE_NAME)

    def get_request(self):
        request = testing.DummyRequest()
        request.context = testing.DummyResource()
        request.db = self.db
        request.rest_resource_url = partial(rest_resource_url, request)
        request.rest_resource_path = partial(rest_resource_path, request)
        return request
