"""
This module contains the base classes for the dashboard and dashboard modules.
"""
from django.db import models

class DashboardPreferences(models.Model):
    """
    This model represents the dashboard preferences for a user.
    """
    user = models.ForeignKey('auth.User')
    data = models.TextField()
    dashboard_id = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s dashboard preferences" % self.user.username

    class Meta:
        db_table = 'admin_tools_dashboard_preferences'
        ordering = ('user',)


# warnings for deprecated imports
from admin_tools.deprecate_utils import import_path_is_changed
from admin_tools.dashboard import dashboards
from admin_tools.dashboard import modules

class Dashboard(
          import_path_is_changed(
              'admin_tools.dashboard.models.Dashboard',
              'admin_tools.dashboard.Dashboard'
          ),
          dashboards.Dashboard
      ): pass

class DefaultIndexDashboard(
          import_path_is_changed(
              'admin_tools.dashboard.models.DefaultIndexDashboard',
              'admin_tools.dashboard.DefaultIndexDashboard',
          ),
          dashboards.DefaultIndexDashboard
      ):pass

class DefaultAppIndexDashboard(
          import_path_is_changed(
              'admin_tools.dashboard.models.DefaultAppIndexDashboard',
              'admin_tools.dashboard.DefaultAppIndexDashboard'
          ),
          dashboards.DefaultAppIndexDashboard
      ):pass

class AppIndexDashboard(
          import_path_is_changed(
              'admin_tools.dashboard.models.AppIndexDashboard',
              'admin_tools.dashboard.AppIndexDashboard'
          ),
          dashboards.AppIndexDashboard
      ):pass


class DashboardModule(
          import_path_is_changed(
              'admin_tools.dashboard.models.DashboardModule',
              'admin_tools.dashboard.modules.DashboardModule',
          ),
          modules.DashboardModule
      ):pass

class AppListDashboardModule(
          import_path_is_changed(
              'admin_tools.dashboard.models.AppListDashboardModule',
              'admin_tools.dashboard.modules.AppList',
          ),
          modules.AppList
      ): pass

class ModelListDashboardModule(
          import_path_is_changed(
              'admin_tools.dashboard.models.ModelListDashboardModule',
              'admin_tools.dashboard.modules.ModelList',
          ),
          modules.ModelList
      ): pass

class LinkListDashboardModule(
          import_path_is_changed(
              'admin_tools.dashboard.models.LinkListDashboardModule',
              'admin_tools.dashboard.modules.LinkList',
          ),
          modules.LinkList
      ): pass

class FeedDashboardModule(
          import_path_is_changed(
              'admin_tools.dashboard.models.FeedDashboardModule',
              'admin_tools.dashboard.modules.Feed',
          ),
          modules.Feed
      ): pass
