from django.test import TestCase

class AdminBasicTest(TestCase):

    def index_page(self, username='staff', password='123'):
        self.assertTrue(self.client.login(username=username, password=password))
        return self.client.get('/admin/')

    def test_admin_loads(self):
        self.assertEqual(self.index_page().status_code, 200)

    def test_permissions(self):
        index = self.index_page()
        self.assertContains(index, 'Foos')
        self.assertNotContains(index, 'Bars')
        self.assertNotContains(index, 'Users')
        self.assertNotContains(index, 'Test app menu')

        super_index = self.index_page('superuser', '123')
        self.assertContains(super_index, 'Users', 3) # menu and dashboard items
        self.assertContains(super_index, 'Test app menu')

    def test_app_index(self):
        self.client.login(username='staff', password='123')
        res = self.client.get('/admin/test_app/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Foos')
        self.assertNotContains(res, 'Bars')

        self.client.login(username='superuser', password='123')
        res = self.client.get('/admin/test_app/')
        self.assertContains(res, 'Foos')
        self.assertContains(res, 'Bars')
        self.assertContains(res, 'Users', 2) # only items from menu

