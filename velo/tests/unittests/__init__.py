# -*- coding: utf-8 -*-
from functools import partial
from unittest import TestCase

from pyramid import testing

from pyramid_rest import rest_resource_path, rest_resource_url
from pyramid_mongokit import mongo_db, mongo_connection

from webob.multidict import MultiDict


class TestBase(TestCase):

    def setUp(self):
        self.config = testing.setUp()
        self.config.include('pyramid_rest')
        self.config.include('velo')

        self.request = testing.DummyRequest()
        self.request.context = testing.DummyResource()
        self.request.rest_resource_url = partial(rest_resource_url,
                                                 self.request)
        self.request.rest_resource_path = partial(rest_resource_path,
                                                  self.request)
        self.request.POST = MultiDict()
        self.request.mongo_connection = mongo_connection(self.request)
        self.request.mongo_db = mongo_db(self.request)

    def tearDown(self):
        testing.tearDown()

    @property
    def db(self):
        return self.request.mongo_db
