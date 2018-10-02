from __future__ import with_statement
import warnings
from unittest import TestCase


class DeprecationTest(TestCase):
    def assertNotDeprecated(self, cls, *args, **kwargs):
        if hasattr(warnings, 'catch_warnings'):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                obj = cls(*args, **kwargs)
                assert len(w) == 0

    def test_dashboard_new(self):
        from admin_tools.dashboard import dashboards

        self.assertNotDeprecated(dashboards.Dashboard)
        self.assertNotDeprecated(dashboards.DefaultIndexDashboard)
        self.assertNotDeprecated(dashboards.DefaultAppIndexDashboard, '', [])
        self.assertNotDeprecated(dashboards.AppIndexDashboard, '', [])

        from admin_tools.dashboard import modules
        self.assertNotDeprecated(modules.DashboardModule)
        self.assertNotDeprecated(modules.AppList)
        self.assertNotDeprecated(modules.ModelList)
        self.assertNotDeprecated(modules.LinkList)
        self.assertNotDeprecated(modules.Feed)

    def test_menu_new(self):
        from admin_tools import menu
        self.assertNotDeprecated(menu.Menu)
        self.assertNotDeprecated(menu.DefaultMenu)

        from admin_tools.menu import items
        self.assertNotDeprecated(items.MenuItem)
        self.assertNotDeprecated(items.AppList)
