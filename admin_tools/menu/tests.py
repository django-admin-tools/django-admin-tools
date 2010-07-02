from tempfile import mktemp
from django.test import TestCase
from django.core import management

from admin_tools.menu.items import AppList

class ManagementCommandTest(TestCase):

    def test_custommenu(self):
        # check that custommenu command doesn't raise exceptions
        file_name = mktemp()
        management.call_command('custommenu', file=file_name)
        # and fails if file is already here
        try:
            management.call_command('custommenu', file=file_name)
            assert False
        except:
            pass


__test__ = {
    'AppList.is_empty': AppList.is_empty,
}
