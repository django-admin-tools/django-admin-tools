from django.test import TestCase

class AdminBasicTest(TestCase):
    def test_admin_loads(self):
        self.assertTrue(self.client.login(username='staff', password='123'))
        res = self.client.get('/admin/')
        self.assertEqual(res.status_code, 200)

    def test_permissions(self):
        self.assertTrue(self.client.login(username='staff', password='123'))
        res = self.client.get('/admin/')
        self.assertContains(res, 'Foos')
        self.assertNotContains(res, 'Bars')
        self.assertNotContains(res, 'Users')

        self.assertTrue(self.client.login(username='superuser', password='123'))
        self.assertContains(self.client.get('/admin/'), 'Users')

    def test_app_index(self):
        self.client.login(username='staff', password='123')
        res = self.client.get('/admin/test_app/foo/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Foos')
        self.assertNotContains(res, 'Bars')

        self.client.login(username='superuser', password='123')
        res = self.client.get('/admin/test_app/foo/')
        self.assertContains(res, 'Foos')
        self.assertContains(res, 'Bars')