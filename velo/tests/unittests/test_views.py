# -*- coding: utf-8 -*-
import unittest

class TestViews(unittest.TestCase):

    def test_index(self):
        from velo.views import index
        result = index(None, None)

        self.assertEqual({'Hello': 'World!'}, result)
