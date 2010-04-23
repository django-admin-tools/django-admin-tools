"""
This module contains the base classes for the dashboard and dashboard modules.
"""

from django.db import models
from admin_tools.dashboard.modules import *
from admin_tools.dashboard.dashboards import *

class DashboardPreferences(models.Model):
    """
    This model represents the dashboard preferences for a user.
    """
    user = models.ForeignKey('auth.User')
    data = models.TextField()

    def __unicode__(self):
        return "%s dashboard preferences" % self.user.username

    class Meta:
        db_table = 'admin_tools_dashboard_preferences'
        ordering = ('user',)


