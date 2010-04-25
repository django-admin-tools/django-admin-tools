from tempfile import mktemp
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.core import management
from django.contrib.auth.models import User, Group

from admin_tools.dashboard import AppIndexDashboard

class ManagementCommandTest(TestCase):
    def test_customdashboard(self):
        # check that customdashboard command doesn't raise exceptions
        file_name = mktemp()
        management.call_command('customdashboard', file=file_name)
        # and fails if file is already here
        try:
            management.call_command('customdashboard', file=file_name)
            assert False
        except:
            pass

class AppIndexDashboardTest(TestCase):
    def test_models(self):
        models = ['django.contrib.auth.models.User',
                  'django.contrib.auth.models.Group']
        board = AppIndexDashboard('Auth', models)
        self.assertEqual(board.get_app_model_classes(), [User, Group])
