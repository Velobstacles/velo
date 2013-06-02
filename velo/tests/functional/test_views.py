from . import TestController


class Test(TestController):

    def test_health(self):
        self.app.get('/health')

    def test_index(self):
        self.app.get('/')
