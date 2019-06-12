from tempfile import mktemp
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.core import management
from django.contrib.auth import models as auth_models

from admin_tools.dashboard import AppIndexDashboard
from admin_tools.dashboard.modules import DashboardModule, Group


class ManagementCommandTest(DjangoTestCase):
    def test_customdashboard(self):
        # check that customdashboard command doesn't raise exceptions
        file_name = mktemp()
        management.call_command("customdashboard", file_name)
        # and fails if file is already here
        try:
            management.call_command("customdashboard", file_name)
            assert False
        except Exception:
            pass


class AppIndexDashboardTest(TestCase):
    def test_models(self):
        models = [
            "django.contrib.auth.models.User",
            "django.contrib.auth.models.Group",
        ]
        board = AppIndexDashboard("Auth", models)
        self.assertEqual(
            board.get_app_model_classes(),
            [auth_models.User, auth_models.Group],
        )


__test__ = {
    "DashboardModule.is_empty": DashboardModule.is_empty,
    "DashboardModule.render_css_classes": DashboardModule.render_css_classes,
    "Group.is_empty": Group.is_empty,
}
