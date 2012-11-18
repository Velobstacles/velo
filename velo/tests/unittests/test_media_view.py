# -*- coding: utf-8 -*-
from bson.binary import Binary

from pyramid import testing

from velo.tests.unittests import TestBase


class TestMedia(TestBase):

    def setUp(self):
        super(TestMedia, self).setUp()
        medium = self.db.Medium()
        medium.location = {'latitude': 45.522706, 'longitude': -73.583885}
        medium.save()
        medium.fs.source = Binary(data='asdf')

        self.medium_id = medium._id

    def tearDown(self):
        self.db.medium.remove({})
        testing.tearDown()

    def test_index(self):
        from velo.views.media import MediaView

        request = self.get_request()
        request.context = testing.DummyResource

        view = MediaView(request.context, request)
        self.assertEqual(
            {'data': [self.db.medium.find_one({'_id': self.medium_id})]},
            view.index()
            )
