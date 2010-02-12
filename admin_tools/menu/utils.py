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


def get_menu_bookmarks(request):
    """
    Returns the bookmarked items or raise an exception.
    """
    import urllib
    try:
        import json
    except ImportError:
        # python < 2.6 
        import simplejson as json
    json_str = urllib.unquote(request.COOKIES.get('menu.bookmarks'))
    if json_str is not None:
        return json.loads(json_str)
    return []
