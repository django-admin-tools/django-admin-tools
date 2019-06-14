from tempfile import mktemp
from django.test import TestCase
from django.core import management

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from admin_tools.menu.items import AppList
from admin_tools.menu.models import Bookmark


class ManagementCommandTest(TestCase):
    def test_custommenu(self):
        # check that custommenu command doesn't raise exceptions
        file_name = mktemp()
        management.call_command("custommenu", file_name)
        # and fails if file is already here
        try:
            management.call_command("custommenu", file_name)
            assert False
        except:
            pass


class DeleteBookMarkTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.superuser_credentials = ("superuser", "123")
        self.staff_credentials = ("staff", "123")
        user = User.objects.get(username=self.superuser_credentials[0])
        self.bookmark = Bookmark.objects.create(
            user=user, url="/test/", title="test"
        )
        self.delete_bookmark_url = reverse(
            "admin-tools-menu-remove-bookmark", args=(self.bookmark.id,)
        )

    def _login_user(self, username, password):
        try:
            user = User.objects.get(username=username)
            self.client.force_login(user)
        except AttributeError:  # in Django<1.9
            logged_in = self.client.login(
                username=user.username, password=password
            )
            self.assertTrue(logged_in)

    def test_removing_of_own_bookmark(self):
        self.assertEqual(Bookmark.objects.count(), 1)
        self._login_user(*self.superuser_credentials)
        self.client.post(self.delete_bookmark_url)
        self.assertFalse(Bookmark.objects.count())

    def test_removing_others_bookmark(self):
        self.assertEqual(Bookmark.objects.count(), 1)
        self._login_user(*self.staff_credentials)
        self.client.post(self.delete_bookmark_url)
        self.assertEqual(Bookmark.objects.first(), self.bookmark)


__test__ = {"AppList.is_empty": AppList.is_empty}
