from django.test import TestCase

class AdminBasicTest(TestCase):
    def test_admin_loads(self):
        self.assertTrue(self.client.login(username='user', password='123'))
        res = self.client.get('/admin/')
        self.assertEqual(res.status_code, 200)
