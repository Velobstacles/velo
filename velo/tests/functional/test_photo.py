import pkg_resources
from bson.objectid import ObjectId

from velo.tests.functional import TestController


class Test(TestController):

    def setUp(self):
        from ...model import Photo, Report

        self.report1 = Report.create(
            self.db,
            u'hadrien',
            u'Road blocked',
            -73.583885,
            45.522706,
            ['blocked']
            )

        obj_id = self.report1._id

        self.photo1 = Photo.create(
            self.db,
            obj_id,
            u'bob',
            -73.583885,
            45.522706,
            pkg_resources.resource_stream('velo', 'static/img/trollface.png'),
            'image/png',
            )
        self.photo_id1 = self.photo1._id

        self.photo2 = Photo.create(
            self.db,
            obj_id,
            u'bob',
            -72.583885,
            44.522706,
            pkg_resources.resource_stream('velo', 'static/img/trollface.png'),
            'image/png',
            )
        self.photo_id2 = self.photo2._id

        self.photo3 = Photo.create(
            self.db,
            obj_id,
            u'bob',
            -74.583885,
            46.522706,
            pkg_resources.resource_stream('velo', 'static/img/trollface.png'),
            'image/png',
            )
        self.photo_id3 = self.photo3._id

    def tearDown(self):
        self.db.Photo.collection.remove()

    def test_index(self):
        result = self.app.get('/photos?page=1&page_size=1')

        self.assertIn('photos', result.json)
        self.assertIsInstance(result.json['photos'], list)

        photo = result.json['photos'][0]
        self.assertIn('photo', photo)
        self.assertIn('links', photo)
        self.assertIn('location', photo['photo'])

        location = photo['photo']['location']
        self.assertIn('type', location)
        self.assertIn('coordinates', location)

        self.assertIn('links', result.json)
        self.assertIn('self', result.json['links'])
        self.assertIn('first', result.json['links'])
        self.assertIn('last', result.json['links'])
        self.assertIn('previous', result.json['links'])
        self.assertIn('next', result.json['links'])

    def test_create(self):
        stream = pkg_resources.resource_stream('velo',
                                               'static/img/trollface.jpg')
        params = {
            u'author': self.report1.author,
            u'longitude': -73.583885,
            u'latitude': 45.522706,
            }
        result = self.app.post(
            '/reports/%s/photos' % self.report1._id,
            params=params,
            upload_files=[('content', 'image.png', stream.read())]
            )
        photo_id = ObjectId(result.json['photo']['_id'])
        photo = self.db.Photo.one({'_id': photo_id})

        self.assertIsNotNone(photo)
        self.assertIsNotNone(photo.get_content_grid_out())

    def test_show(self):
        result = self.app.get('/photos/%s' % self.photo_id1)

        self.assertIn('photo', result.json)
        self.assertIn('links', result.json)

        self.assertEqual(str(self.photo_id1), result.json['photo']['_id'])
        self.assertEqual(u'bob', result.json['photo']['author'])

    def test_show_not_an_objectid(self):
        self.app.get('/photos/1234', status=404)

    def test_show_not_found(self):
        self.app.get('/photos/%s' % ObjectId(), status=404)

    def test_delete(self):
        self.app.delete('/photos/%s' % self.photo_id1)

    def test_delete_not_found(self):
        self.app.delete('/photos/%s' % ObjectId(), status=404)
