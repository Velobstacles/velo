import re

from ..functional import TestController


class Test(TestController):

    def setUp(self):
        from ...model import User, Report
        self.user1 = User.create(
            self.db,
            u'Bob Marley',
            u'bob',
            u'bob@trenchtown.com',
            u'sense',
            )
        self.report1 = Report.create(
            self.db,
            u'bob',
            u'Road blocked',
            -73, 45,
            ['blocked']
            )

    def tearDown(self):
        self.db.User.collection.drop()
        self.db.Report.collection.drop()

    def test_create(self):
        from ...model import Report
        params = {
            u'longitude': -73.583885,
            u'latitude': 45.522706,
            u'description': 'wow a description',
            u'tags': ['broken', 'blocked']
            }
        result = self.app.post('/users/%s/reports/' % self.user1._id,
                               params=params)

        location_re = re.compile(r'http://localhost/reports/([a-f0-9]{24})/')
        location = result.headers.getone('Location')
        self.assertRegexpMatches(location, location_re)

        report_id = location_re.findall(location).pop()

        report = Report.get_by_id(self.db, report_id)
        self.assertIsNotNone(report)

        self.assertEqual('bob', report.author)
        self.assertEqual([-73.583885, 45.522706], report.location.coordinates)
        self.assertEqual(u'wow a description', report.description)
        self.assertEqual([u'broken', u'blocked'], report.tags)

        expected = {
            u'links': {
                u'self': unicode(location),
                u'photos': u'%sphotos/' % location,
                },
            u'report': {
                u'_id': unicode(report_id),
                u'author': u'bob',
                u'description': u'wow a description',
                u'created': unicode(report._id.generation_time.isoformat()),
                u'tags': [u'broken', u'blocked'],
                u'location': {
                    u'type': u'Point',
                    u'coordinates': [-73.583885, 45.522706]
                    }
                }
            }
        self.assertEqual(expected, result.json)

    def test_index(self):
        result = self.app.get('/users/%s/reports/' % self.user1._id)

        created = self.report1._id.generation_time

        report = {
            "description": "Road blocked",
            "created": created.isoformat(),
            "tags": ["blocked"],
            "location": {
                "type": "Point",
                "coordinates": [-73, 45]
                },
            "author": "bob",
            "_id": str(self.report1._id),
            }
        self.assertEqual(report, result.json['reports'][0]['report'])

        self.assertUrlEqual(
            'http://localhost/reports/%s/' % self.report1._id,
            result.json['reports'][0]['links']['self']
            )

        self.assertUrlEqual(
            'http://localhost/reports/%s/photos/' % self.report1._id,
            result.json['reports'][0]['links']['photos']
            )

        self.assertUrlEqual(
            'http://localhost/users/%s/reports/?limit=20&offset=0' %
                self.user1._id,
            result.json['links']['self']
            )
