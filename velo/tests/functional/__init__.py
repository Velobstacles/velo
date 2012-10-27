# -*- coding: utf-8 -*-
import unittest

import webtest

import velo

settings = {}


class TestController(unittest.TestCase):

    _app = None

    @property
    def app(self):
        if TestController._app is None:
            TestController._app = velo.main(None, **settings)
        return webtest.TestApp(TestController._app)
