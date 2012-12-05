# -*- coding: utf-8 -*-
import unittest

import webtest

settings = {
    'mako.directories': 'velo:templates',
    }


class TestController(unittest.TestCase):

    _app = None

    @property
    def app(self):
        if TestController._app is None:
            import velo
            TestController._app = velo.main(None, **settings)
        return webtest.TestApp(TestController._app)
