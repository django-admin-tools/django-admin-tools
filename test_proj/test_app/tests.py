from django.test import TestCase

class AdminBasicTest(TestCase):
    fixtures = ['users.json']
    def test_admin_loads(self):
        c = self.client
        self.assertTrue(c.login(username='user', password='123'))
        res = c.get('/admin/')
        self.assertEqual(res.status_code, 200)
