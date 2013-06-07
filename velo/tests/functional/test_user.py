import re

from ..functional import TestController


class Test(TestController):

    def setUp(self):
        from ...model import User
        self.user1 = User.create(
            self.db,
            u'Hadrien David',
            u'hadrien',
            u'hadrien@ectobal.com',
            u'password',
            )

    def tearDown(self):
        self.db.User.collection.drop()

    def test_index(self):
        result = self.app.get('/users/')
        created = unicode(self.user1._id.generation_time.isoformat())
        expected = {
            u"users": [{
                u"user": {
                    u"username": u"hadrien",
                    u"_id": unicode(self.user1._id),
                    u"name": u"Hadrien David",
                    u"created": created,
                    u"mail": u"hadrien@ectobal.com",
                    },
                u"links": {
                    u"self": u"http://localhost/users/%s/" % self.user1._id,
                    },
                }],
            u"links": {
                u"self": u"http://localhost/users/?offset=0&limit=20",
                u"last": u"http://localhost/users/?offset=0&limit=20",
                u"first": u"http://localhost/users/?offset=0&limit=20",
                }
            }

        self.assertEqual(expected['users'][0]['user'],
                         result.json['users'][0]['user'])
        self.assertEqual(expected['users'][0]['links'],
                         result.json['users'][0]['links'])

        self.assertUrlEqual(expected['links']['self'],
                            result.json['links']['self'])
        self.assertUrlEqual(expected['links']['last'],
                            result.json['links']['last'])
        self.assertUrlEqual(expected['links']['first'],
                            result.json['links']['first'])

    def test_create(self):
        from ...model import User
        params = {
            u'username': u'bob_marley2000',
            u'name': u'Bob Marley',
            u'password': u'trenchtown',
            u'mail': u'bob@marley.com',
            }
        result = self.app.post('/users/', params=params)

        location_re = re.compile(r'http://localhost/users/([a-f0-9]{24})/')
        location = result.headers.getone('Location')
        self.assertRegexpMatches(location, location_re)

        bob_id = location_re.findall(location).pop()
        bob = User.get_by_id(self.db, bob_id)

        expected = {
            u"user": {
                u"username": u"bob_marley2000",
                u"mail": u"bob@marley.com",
                u"name": u"Bob Marley",
                u"_id": unicode(bob_id),
                u"created": unicode(bob._id.generation_time.isoformat()),
                },
            u"links": {
                "self": location,
                }
            }

        self.assertEqual(expected, result.json)

    def test_create_duplicate_username(self):
        from pyramid.httpexceptions import HTTPConflict
        params = {
            u'username': u'hadrien',
            u'name': u'Bob Marley',
            u'password': u'trenchtown',
            u'mail': u'bob@marley.com',
            }
        self.app.post('/users/', params=params, status=HTTPConflict.code)
