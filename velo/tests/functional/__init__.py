import unittest

import webtest

from pyramid.decorator import reify

from pyramid_mongokit import get_mongo_connection

settings = {
    'mako.directories': 'velo:templates',
    }


class TestController(unittest.TestCase):

    maxDiff = None

    @reify
    def config(self):
        from pyramid.config import Configurator
        config = Configurator(settings=settings)
        config.include('velo')
        return config

    @reify
    def app(self):
        return webtest.TestApp(self.config.make_wsgi_app())

    @reify
    def db(self):
        return self.connection.get_db()

    @reify
    def connection(self):
        return get_mongo_connection(self.config.registry)
