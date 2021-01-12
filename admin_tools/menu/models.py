"""
This module contains the base classes for menu and menu items.
"""
import sys

from django.conf import settings
from django.db import models

# for backward-compatibility
from admin_tools import menu
from admin_tools.menu import items
from admin_tools.deprecate_utils import import_path_is_changed

user_model = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


class Bookmark(models.Model):
    """
    This model represents a user created bookmark.
    """
    user = models.ForeignKey(user_model, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)

    def __str__(self):
        return "%s - %s" % (self.title, self.url)

    if sys.version_info[0] == 2:
        __unicode__ = __str__
        del __str__

    class Meta:
        db_table = 'admin_tools_menu_bookmark'
        ordering = ('id',)


class Menu(
          import_path_is_changed(
              'admin_tools.menu.models.Menu',
              'admin_tools.menu.Menu'
          ),
          menu.Menu
      ):
    pass


class DefaultMenu(
          import_path_is_changed(
              'admin_tools.menu.models.DefaultMenu',
              'admin_tools.menu.DefaultMenu'
          ),
          menu.DefaultMenu
      ):
    pass


class MenuItem(
          import_path_is_changed(
              'admin_tools.menu.models.MenuItem',
              'admin_tools.menu.items.MenuItem'
          ),
          items.MenuItem
      ):
    pass


class AppListMenuItem(
          import_path_is_changed(
              'admin_tools.menu.models.AppListMenuItem',
              'admin_tools.menu.items.AppList'
          ),
          items.AppList
      ):
    pass


class BookmarkMenuItem(
          import_path_is_changed(
              'admin_tools.menu.models.BookmarkMenuItem',
              'admin_tools.menu.items.Bookmarks'
          ),
          items.Bookmarks
      ):
    pass
