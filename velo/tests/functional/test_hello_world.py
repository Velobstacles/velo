# -*- coding: utf-8 -*-
from velo.tests.functional import TestController


class TestHelloWorld(TestController):

    def test_hello_index(self):

        result = self.app.get('/hello_world')

        self.assertEqual('application/json', result.content_type)
        self.assertEqual({"Hello": "World!"}, result.json_body)
