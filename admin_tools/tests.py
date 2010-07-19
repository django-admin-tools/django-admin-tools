from __future__ import with_statement
import warnings
from unittest import TestCase

class DeprecationTest(TestCase):
    # python >= 2.6 is required to make deprecation warning tests useful
    # this DeprecationTest is always successful for python < 2.6

    def assertDeprecated(self, cls, *args, **kwargs):
        if hasattr(warnings, 'catch_warnings'):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                obj = cls(*args, **kwargs)

                assert len(w) == 1
                assert issubclass(w[-1].category, DeprecationWarning)
                assert "deprecated" in str(w[-1].message)


    def assertNotDeprecated(self, cls, *args, **kwargs):
        if hasattr(warnings, 'catch_warnings'):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                obj = cls(*args, **kwargs)
                assert len(w) == 0


    def test_dashboard(self):
        from admin_tools.dashboard import models

        self.assertDeprecated(models.Dashboard)
        self.assertDeprecated(models.DefaultIndexDashboard)
        self.assertDeprecated(models.DefaultAppIndexDashboard, '', [])
        self.assertDeprecated(models.AppIndexDashboard, '', [])

        self.assertDeprecated(models.DashboardModule)
        self.assertDeprecated(models.AppListDashboardModule)
        self.assertDeprecated(models.ModelListDashboardModule)
        self.assertDeprecated(models.LinkListDashboardModule)
        self.assertDeprecated(models.FeedDashboardModule)

    def test_dashboard_new(self):
        from admin_tools import dashboard

        self.assertNotDeprecated(dashboard.Dashboard)
        self.assertNotDeprecated(dashboard.DefaultIndexDashboard)
        self.assertNotDeprecated(dashboard.DefaultAppIndexDashboard, '', [])
        self.assertNotDeprecated(dashboard.AppIndexDashboard, '', [])

        from admin_tools.dashboard import modules
        self.assertNotDeprecated(modules.DashboardModule)
        self.assertNotDeprecated(modules.AppList)
        self.assertNotDeprecated(modules.ModelList)
        self.assertNotDeprecated(modules.LinkList)
        self.assertNotDeprecated(modules.Feed)


    def test_menu(self):
        from admin_tools.menu import models
        self.assertDeprecated(models.Menu)
        self.assertDeprecated(models.DefaultMenu)
        self.assertDeprecated(models.MenuItem)
        self.assertDeprecated(models.AppListMenuItem)
        self.assertDeprecated(models.BookmarkMenuItem)

    def test_menu_new(self):
        from admin_tools import menu
        self.assertNotDeprecated(menu.Menu)
        self.assertNotDeprecated(menu.DefaultMenu)

        from admin_tools.menu import items
        self.assertNotDeprecated(items.MenuItem)
        self.assertNotDeprecated(items.AppList)
        self.assertNotDeprecated(items.Bookmarks)
