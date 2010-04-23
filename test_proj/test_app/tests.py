from django.test import TestCase

class AdminBasicTest(TestCase):
    def test_admin_loads(self):
        self.client.get('/admin/')