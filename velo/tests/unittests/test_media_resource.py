import unittest
import pkg_resources

from cgi import FieldStorage

from pyramid import testing
from pyramid.httpexceptions import HTTPNotFound

from velo.tests.unittests import TestBase


@unittest.skip('No more views because changing from url dispatch to traversal')
class TestMedia(TestBase):

    def setUp(self):
        super(TestMedia, self).setUp()
        medium = self.db.Medium()
        medium.location = {'latitude': 45.522706, 'longitude': -73.583885}
        medium.mime_type = u'image/png'
        medium.save()
        fp = pkg_resources.resource_stream('velo', 'static/img/trollface.png')
        medium.fs.put(fp, filename='content')

        self.medium_id = medium._id

    def get_collection(self):
        from velo.resources import Root
        root = Root(self.request)
        return root['media']

    def tearDown(self):
        super(TestMedia, self).tearDown()
        self.db.medium.remove({})
        testing.tearDown()

    def test_index(self):
        collection = self.get_collection()
        result = list(collection.index())

        self.assertEqual(1, len(result))
        item = result[0]
        medium = self.db.Medium.find_one({'_id': self.medium_id})

        self.assertEqual(medium._id, item.model['_id'])
        self.assertEqual(medium.location, item.model['location'])
        self.assertEqual(item, item.links['self'])

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
            u'velo',
            u'static/img/trollface.png'
            )
        view.request.POST.update({
            u'longitude': 12.3,
            u'latitude': -45.4,
            u'content': content,
            })
        view.create()

    def test_update(self):
        self.get_view()
