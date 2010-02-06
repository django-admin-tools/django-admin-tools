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
    menu_cls = getattr(settings, 'ADMIN_TOOLS_MENU', False)
    if menu_cls:
        try:
            mod, inst = menu_cls.rsplit('.', 1)
            mod = import_module(mod)
            return getattr(mod, inst)()
        except:
            raise ImproperlyConfigured((
                'The class pointed by your ADMIN_TOOLS_MENU setting variable '
                'cannot be imported'
            ))

    admin_menu = Menu()
    admin_menu.append(MenuItem(
        title=_('Dashboard'),
        url=reverse('admin:index')
    ))
    admin_menu.append(AppListMenuItem(
        title=_('Applications'),
        exclude_list=('django.contrib',),
    ))
    admin_menu.append(AppListMenuItem(
        title=_('Administration'),
        include_list=('django.contrib',),
    ))
    return admin_menu
