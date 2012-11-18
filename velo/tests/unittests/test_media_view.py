# -*- coding: utf-8 -*-
from bson.binary import Binary

from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from velo.tests.unittests import TestBase


class TestMedia(TestBase):

    def setUp(self):
        super(TestMedia, self).setUp()
        medium = self.db.Medium()
        medium.location = {'latitude': 45.522706, 'longitude': -73.583885}
        medium.save()
        medium.fs.source = Binary(data='asdf')

        self.medium_id = medium._id

    def get_view(self):
        from velo.views.media import MediaView
        request = self.get_request()
        return MediaView(request.context, request)

    def tearDown(self):
        self.db.medium.remove({})
        testing.tearDown()

    def test_index(self):
        view = self.get_view()
        result = view.index()

        self.assertTrue('data' in result)
        data = result['data']

        self.assertEqual(1, len(data))
        data = data[0]
        medium = self.db.Medium.find_one({'_id': self.medium_id})

        self.assertEqual(str(medium._id), data['id'])
        self.assertEqual(medium.location, data['location'])
        self.assertEqual(
            u'http://example.com/media/%s' % str(medium._id),
            data['links']['self'],
            )

    def test_show_404(self):
        view = self.get_view()
        self.assertRaises(HTTPNotFound, view.show, '123')
        self.assertRaises(HTTPNotFound, view.show, '50a85b229978d063d7a3dd04')

    def test_show(self):
        view = self.get_view()
        result = view.show(self.medium_id)
        self.assertTrue(result)
