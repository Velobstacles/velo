import unittest

import webtest

from pyramid.decorator import reify

from pyramid_mongokit import get_mongo_connection

settings = {
    'mako.directories': 'velo:templates',
    }


def setUpPackage():
    from pyramid.config import Configurator
    TestController.config = Configurator(settings=settings)
    TestController.config.include('velo')


class TestController(unittest.TestCase):

    _app = None

    @property
    def app(self):
        if TestController._app is None:
            TestController._app = TestController.config.make_wsgi_app()
        return webtest.TestApp(TestController._app)

    @reify
    def db(self):
        return self.connection.get_db()

    @reify
    def connection(self):
        return get_mongo_connection(TestController.config.registry)
