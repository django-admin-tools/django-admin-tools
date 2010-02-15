"""
Menu utilities.
"""

import urllib
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
        'admin_tools.menu.models.DefaultMenu'
    )
    try:
        mod, inst = menu_cls.rsplit('.', 1)
        mod = import_module(mod)
    except Exception, exc:
        raise ImproperlyConfigured((
            'The class pointed by your ADMIN_TOOLS_MENU setting variable '
            'cannot be imported: %s' % exc.message
        ))
    return getattr(mod, inst)()
