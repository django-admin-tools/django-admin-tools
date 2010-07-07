"""
Menu utilities.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def get_admin_menu():
    """
    Returns the admin menu defined by the user or the default one.
    """
    menu_cls = getattr(
        settings,
        'ADMIN_TOOLS_MENU',
        'admin_tools.menu.DefaultMenu'
    )
    mod, inst = menu_cls.rsplit('.', 1)
    mod = import_module(mod)
    return getattr(mod, inst)()
