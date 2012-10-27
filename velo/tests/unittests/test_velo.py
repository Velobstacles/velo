# -*- coding: utf-8 -*-
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

        Configurator.assert_called_once_with(settings={'param': 'value'})

        config.include.assert_called_once_with('pyramid_rest')
        config.scan.assert_called_once_with('velo.views')
        config.make_wsgi_app.assert_called_once_with()
