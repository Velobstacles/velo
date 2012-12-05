# -*- coding: utf-8 -*-
import pkg_resources

from cgi import FieldStorage

from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from velo.tests.unittests import TestBase


class TestMedia(TestBase):

    def setUp(self):
        super(TestMedia, self).setUp()
        medium = self.db.Medium()
        medium.location = {'latitude': 45.522706, 'longitude': -73.583885}
        medium.mime_type = 'image/png'
        medium.save()
        fp = pkg_resources.resource_stream('velo', 'static/img/trollface.png')
        medium.fs.put(fp, filename='content')

        self.medium_id = medium._id

    def get_view(self):
        from velo.views.media import MediaView
        request = self.get_request()
        return MediaView(request.context, request)

    def tearDown(self):
        super(TestMedia, self).tearDown()
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
        medium = self.db.Medium.find_one({'_id': self.medium_id})
        view = self.get_view()
        result = view.show(str(self.medium_id))
        self.assertTrue(result)
        self.assertEqual(medium.location, result['location'])
        self.assertEqual(str(medium._id), result['id'])
        self_link = 'http://example.com/media/%s' % self.medium_id
        self.assertEqual(
            {'self': self_link, 'content': self_link + '/content'},
            result['links'],
            )
        self.assertEqual(5, len(result.keys()))

    def test_create(self):
        view = self.get_view()
        content = FieldStorage()
        content.file = pkg_resources.resource_stream(
            'velo',
            'static/img/trollface.png'
            )
        view.request.POST.update({
            'longitude': 12.3,
            'latitude': -45.4,
            'content': content,
            })
        view.create()

    def test_update(self):
        self.get_view()
