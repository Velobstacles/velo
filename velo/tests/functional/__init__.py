import unittest
import urlparse

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

    def assertUrlEqual(self, url1, url2):
        u1 = urlparse.urlparse(url1)
        u2 = urlparse.urlparse(url2)

        for attr in ['scheme', 'netloc', 'path', 'params', 'fragment']:
            attr1 = getattr(u1, attr)
            attr2 = getattr(u2, attr)
            if attr1 != attr2:
                msg = 'AssertionError: %s != %s. %s != %s'
                self.fail(msg % (attr1, attr2, url1, url2))

        q1 = urlparse.parse_qs(u1.query)
        q2 = urlparse.parse_qs(u2.query)
        if q1 != q2:
            msg = 'AssertionError: %s != %s. %s != %s'
            self.fail(msg % (q1, q2, url1, url2))
