import pkg_resources

from velo.tests.functional import TestController


class Test(TestController):

    def setUp(self):
        from ...model.report import Report
        from ...model.photo import Photo
        self.report1 = Report.create(
            self.db,
            u'hadrien',
            u'Road blocked',
            1, 1,
            ['blocked']
            )
        self.photo1 = Photo.create(
            self.db,
            self.report1._id,
            u'bob',
            -73.583885,
            45.522706,
            pkg_resources.resource_stream('velo', 'static/img/trollface.png'),
            'image/png',
            )

        self.report2 = Report.create(
            self.db,
            u'hadrien',
            u'Road disappeared 2',
            2, 2,
            ['disappeared']
            )

    def tearDown(self):
        self.db.Report.collection.drop()
        self.db.Photo.collection.drop()

    def test_index(self):
        result = self.app.get('/reports?location=1.0%2C1.0')

        self.assertIn('links', result.json)
        self.assertIn('reports', result.json)

        links = result.json['links']
        self.assertEqual(
            'http://localhost/reports/'
            '?radius=50&location=1.0%2C1.0&page_size=20&page=0',
            links['self'],
            )
        self.assertEqual(
            'http://localhost/reports/'
            '?radius=50&location=1.0%2C1.0&page_size=20&page=0',
            links['last'],
            )
        self.assertEqual(
            'http://localhost/reports/'
            '?radius=50&location=1.0%2C1.0&page_size=20&page=0',
            links['first'],
            )

        reports = result.json['reports']
        print reports

    def test_report(self):
        self.app.get('/reports/%s' % self.report1._id)

        self.app.get('/reports/%s/photos/' % self.report1._id)
        print self.app.get('/reports/%s/photos/%s' % (self.report1._id,
                                                      self.photo1._id))
