"""
This module contains the base classes for menu and menu items.
"""
from django.db import models

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

# for backward-compatibility
from admin_tools import menu
from admin_tools.menu import items
from admin_tools.deprecate_utils import import_path_is_changed

class Menu(
          import_path_is_changed(
              'admin_tools.menu.models.Menu',
              'admin_tools.menu.Menu'
          ),
          menu.Menu
      ): pass

class DefaultMenu(
          import_path_is_changed(
              'admin_tools.menu.models.DefaultMenu',
              'admin_tools.menu.DefaultMenu'
          ),
          menu.DefaultMenu
      ): pass

class MenuItem(
          import_path_is_changed(
              'admin_tools.menu.models.MenuItem',
              'admin_tools.menu.items.MenuItem'
          ),
          items.MenuItem
      ): pass

class AppListMenuItem(
          import_path_is_changed(
              'admin_tools.menu.models.AppListMenuItem',
              'admin_tools.menu.items.AppList'
          ),
          items.AppList
      ): pass

class BookmarkMenuItem(
          import_path_is_changed(
              'admin_tools.menu.models.BookmarkMenuItem',
              'admin_tools.menu.items.Bookmarks'
          ),
          items.Bookmarks
      ): pass
