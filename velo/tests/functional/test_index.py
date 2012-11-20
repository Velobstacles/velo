# -*- coding: utf-8 -*-
from __future__ import absolute_import
from velo.tests.functional import TestController


class TestHelloWorld(TestController):

    def test_index(self):

        result = self.app.get('/')

        self.assertEqual('text/html', result.content_type)
