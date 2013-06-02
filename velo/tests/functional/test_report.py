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

    def test_index_filtered_by_location(self):
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

        self.assertEqual(1, len(reports))

        report = reports[0]

        expected = {
            u"links": {
                u"self": u"http://localhost/reports/%s/" % self.report1._id,
                u"photos": (u"http://localhost/reports/%s/photos/"
                            % self.report1._id
                            ),
                },
            u"report": {
                u"_id": unicode(self.report1._id),
                u"created": unicode(
                    self.report1._id.generation_time.isoformat()
                    ),
                u"description": u'Road blocked',
                u"author": u"hadrien",
                u"location": {
                    u"type": u"Point",
                    u"coordinates": [1, 1],
                    },
                u"tags": [u"blocked"],
                },
            }

        self.assertEqual(expected, report)

    def test_index(self):
        result = self.app.get('/reports')

        self.assertIn('links', result.json)
        self.assertIn('reports', result.json)

        links = result.json['links']

        expected = {
            u"self": u"http://localhost/reports/?page=0&page_size=20",
            u"first": u"http://localhost/reports/?page=0&page_size=20",
            u"last": u"http://localhost/reports/?page=0&page_size=20",
            }

        self.assertEqual(expected, links)

    def test_report(self):
        result = self.app.get('/reports/%s' % self.report1._id)

        expected = {
            u"links": {
                u"self": u"http://localhost/reports/%s/" % self.report1._id,
                u"photos": (u"http://localhost/reports/%s/photos/"
                            % self.report1._id
                            ),
                },
            u"report": {
                u"_id": unicode(self.report1._id),
                u"created": unicode(
                    self.report1._id.generation_time.isoformat()
                    ),
                u"description": u'Road blocked',
                u"author": u"hadrien",
                u"location": {
                    u"type": u"Point",
                    u"coordinates": [1, 1],
                    },
                u"tags": [u"blocked"],
                },
            }

        self.assertEqual(expected, result.json)

    def test_report_photos(self):
        result = self.app.get('/reports/%s/photos/' % self.report1._id)

        r_id = unicode(self.report1._id)
        p_id = unicode(self.photo1._id)

        expected = {
            u'links': {
                u'first': u'http://localhost/reports/%s/photos/'
                          '?page=0&page_size=20' % r_id,
                u'last': u'http://localhost/reports/%s/photos/'
                          '?page=0&page_size=20' % r_id,
                u'self': u'http://localhost/reports/%s/photos/'
                          '?page=0&page_size=20' % r_id,
                },
            u'photos': [{
                u'links': {
                    u'content': u'http://localhost/photos/%s/content/' % p_id,
                    u'report': u'http://localhost/reports/%s/' % r_id,
                    u'self': u'http://localhost/photos/%s/' % p_id,
                    },
                u'photo': {
                    u'_id': unicode(p_id),
                    u'author': u'bob',
                    u'location': {
                        u'coordinates': [-73.583885, 45.522706],
                        u'type': u'Point'
                        },
                    u'report_id': r_id
                    }
                }]
            }
        self.assertEqual(expected, result.json)
