"""
Menu utilities.
"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu.models import Menu, MenuItem, AppListMenuItem


def get_admin_menu(request):
    """
    Returns the admin menu defined by the user or the default one.
    """
    provider = getattr(settings, 'ADMIN_TOOLS_INDEX_MENU_PROVIDER', False)
    if provider:
        from django.utils.importlib import import_module
        mod, inst = provider.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)()

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
