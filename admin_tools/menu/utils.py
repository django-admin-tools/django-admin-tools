"""
Menu utilities.
"""

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.importlib import import_module
from admin_tools.menu.models import Menu, MenuItem, AppListMenuItem


def get_admin_menu(request):
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
    except:
        raise ImproperlyConfigured((
            'The class pointed by your ADMIN_TOOLS_MENU setting variable '
            'cannot be imported'
        ))
    return getattr(mod, inst)()
