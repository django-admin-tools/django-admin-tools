from tempfile import mkstemp, mktemp
from django.test import TestCase
from django.core import management

class ManagementCommandTest(TestCase):
    def test_customdashboard(self):
        # check that customdashboard command don't raise exceptions
        file_name = mktemp()
        management.call_command('customdashboard', file=file_name)
        # and fails if file is already here
        try:
            management.call_command('customdashboard', file=file_name)
            assert False
        except:
            pass

