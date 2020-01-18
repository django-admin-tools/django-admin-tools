import sys
import json

from django.test import TestCase
from django.contrib.auth.models import User
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse

from admin_tools.dashboard.models import DashboardPreferences
from admin_tools.menu.models import Bookmark


class AdminBasicTest(TestCase):

    fixtures = ['users.json']

    def _login(self, username, password):
        try:
            user = User.objects.get(username=username)
            self.client.force_login(user)
        except AttributeError:  # in Django<1.9
            self.client.login(username=username, password=password)

    def test_admin_loads(self):
        for (username, password) in (('superuser', '123'), ('staff', '123')):
            self._login(username, password)
            response = self.client.get('/admin/')
            self.assertEqual(response.status_code, 200)
            self.client.logout()

    def test_custom_menu_media(self):
        self._login('superuser', '123')
        response = self.client.get('/admin/')
        self.assertContains(response, '<link rel="stylesheet" href="/static/test_app/menu.css" type="text/css" media="all"/>')
        self.assertContains(response, '/static/test_app/menu.js')
        self.client.logout()

    def test_custom_dashboard_media(self):
        self._login('superuser', '123')
        response = self.client.get('/admin/')
        self.assertContains(response, '<link rel="stylesheet" href="/static/test_app/dashboard.css" type="text/css" media="all"/>')
        self.assertContains(response, '/static/test_app/dashboard.js')
        self.client.logout()

    def test_permissions(self):
        self._login('staff', '123')
        index = self.client.get('/admin/')
        self.assertContains(index, 'Bars')
        self.assertNotContains(index, 'Foos')
        self.assertNotContains(index, 'Users')
        self.assertContains(index, 'Test app menu')
        self.client.logout()

        self._login('superuser', '123')
        super_index = self.client.get('/admin/')
        self.assertContains(super_index, 'Bars')
        self.assertContains(super_index, 'Foos')
        self.assertContains(super_index, 'Test app menu')
        self.assertContains(super_index, 'Users', 4) # menu and dashboard items
        self.client.logout()
        self.client.logout()

    def test_app_index(self):
        self._login('staff', '123')
        res = self.client.get('/admin/test_app/')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Bars')
        self.assertNotContains(res, 'Foos')
        self.client.logout()

        self._login('superuser', '123')
        res = self.client.get('/admin/test_app/')
        self.assertContains(res, 'Foos')
        self.assertContains(res, 'Bars')
        self.assertContains(res, 'Users', 2) # only items from menu

    def test_add_dashboard_preferences(self):
        self._login('superuser', '123')
        pref_data = {"foo": "bar"}
        res = self.client.post(
            reverse('admin-tools-dashboard-set-preferences', args=('test-dashboard',)),
            {'data': json.dumps(pref_data)}
        )
        self.assertEqual(res.status_code, 200)
        pref = DashboardPreferences.objects.get(dashboard_id='test-dashboard')
        self.assertEqual(json.loads(pref.data), pref_data)

    def test_edit_dashboard_preferences(self):
        try:
            user = User.objects.get(username='superuser')
            self.client.force_login(user)
        except AttributeError:  # in Django<1.9
            self.client.login(username='superuser', password='123')
        self._login('superuser', '123')
        user = User.objects.get(username='superuser')
        pref = DashboardPreferences.objects.create(
            user=user,
            dashboard_id='test-dashboard',
            data=json.dumps('{}')
        )
        new_pref_data = {"bar": "baz"}
        res = self.client.post(
            reverse('admin-tools-dashboard-set-preferences', args=('test-dashboard',)),
            {'data': json.dumps(new_pref_data)}
        )
        self.assertEqual(res.status_code, 200)
        pref = DashboardPreferences.objects.get(pk=pref.pk)
        self.assertEqual(json.loads(pref.data), new_pref_data)

    def test_add_menu_bookmark(self):
        self._login('superuser', '123')
        res = self.client.post(
            reverse('admin-tools-menu-add-bookmark'),
            {'url': '/admin/', 'title': 'Admin site'}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Added')

    def test_edit_menu_bookmark(self):
        self._login('superuser', '123')
        user = User.objects.get(username='superuser')
        bm = Bookmark.objects.create(user=user, url='/admin/', title='Test bookmark')
        new_title = 'Test bookmark updated !'
        res = self.client.post(
            reverse('admin-tools-menu-edit-bookmark', args=(bm.pk,)),
            {'url': '/admin/', 'title': new_title}
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Saved')
        bm = Bookmark.objects.get(pk=bm.pk)
        self.assertEqual(bm.title, new_title)

    def test_remove_menu_bookmark(self):
        self._login('superuser', '123')
        user = User.objects.get(username='superuser')
        bm = Bookmark.objects.create(user=user, url='/admin/', title='Test bookmark')
        res = self.client.get(
            reverse('admin-tools-menu-remove-bookmark', args=(bm.pk,))
        )
        self.assertContains(res, 'Are you sure you want to delete this bookmark')

        res = self.client.post(
            reverse('admin-tools-menu-remove-bookmark', args=(bm.pk,))
        )
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Deleted')
        with self.assertRaises(Bookmark.DoesNotExist):
            Bookmark.objects.get(pk=bm.pk)

