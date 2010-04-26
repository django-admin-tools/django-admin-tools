"""
This module contains the base classes for menu and menu items.
"""
from django.db import models

# for backward-compatibility
from admin_tools.menu.menus import *
from admin_tools.menu.items import *

class Bookmark(models.Model):
    """
    This model represents a user created bookmark.
    """
    user = models.ForeignKey('auth.User')
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s - %s" % (self.title, self.url)

    class Meta:
        db_table = 'admin_tools_menu_bookmark'
        ordering = ('id',)

