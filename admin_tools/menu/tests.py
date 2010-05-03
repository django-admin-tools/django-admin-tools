from tempfile import mktemp
from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.core import management

class ManagementCommandTest(TestCase):
    def test_customdashboard(self):
        # check that customdashboard command doesn't raise exceptions
        file_name = mktemp()
        management.call_command('custommenu', file=file_name)
        # and fails if file is already here
        try:
            management.call_command('custommenu', file=file_name)
            assert False
        except:
            pass
