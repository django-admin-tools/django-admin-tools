"""
This module contains the base classes for menu and menu items.
"""

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
