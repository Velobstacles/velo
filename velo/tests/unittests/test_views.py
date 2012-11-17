# -*- coding: utf-8 -*-
import unittest

import mock


class TestViews(unittest.TestCase):

    def test_index(self):
        from velo.views import index
        result = index(None, None)

        self.assertEqual({}, result)

    def test_base(self):
        from velo.views import Base
        req = mock.Mock()
        ctx = mock.Mock

        b = Base(ctx, req)

        self.assertEqual(req, b.request)
        self.assertEqual(ctx, b.context)
