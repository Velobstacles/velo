# -*- coding: utf-8 -*-
from __future__ import absolute_import
import unittest

import mock


class TestMain(unittest.TestCase):

    @mock.patch('velo.Configurator')
    def test_main(self, Configurator):
        from velo import main

        result = main({}, param='value')

        config = Configurator.return_value

        self.assertEqual(
            config.make_wsgi_app.return_value,
            result
            )
