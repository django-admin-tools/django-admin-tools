"""
Menu template tags, the following menu tags are available:
* ``{% render_menu %}``
* ``{% render_menu_item %}``
* ``{% render_menu_js %}``
* ``{% render_menu_css %}``

To load the menu tags just do: ``{% load menu_tags %}``.
"""

from django import template
from django.http import HttpRequest
from admin_tools.utils import render_media
from admin_tools.menu.utils import get_admin_menu

register = template.Library()

def render_menu(context, menu=None):
    """
    Template tag that renders the menu, it takes an optional ``Menu`` instance
    as unique argument, if not given, the menu will be retrieved with the
    ``get_admin_menu`` function.
    """
    if menu is None:
        menu = get_admin_menu(context['request'])
    context.update({
        'template': menu.template,
        'menu': menu,
    })
    return context
render_menu = register.inclusion_tag(
    'menu/dummy.html',
    takes_context=True
)(render_menu)


def render_menu_item(context, item, index=None):
    """
    Template tag that renders a given menu item, it takes a ``MenuItem``
    instance as unique parameter.
    """
    item.render(context['request'])
    context.update({
        'template': item.template,
        'item': item,
        'index': index,
    })
    return context
render_menu_item = register.inclusion_tag(
    'menu/dummy.html',
    takes_context=True
)(render_menu_item)


def render_menu_js(menu=None):
    """
    Template tag that renders the needed js files for the menu.
    It relies on the ``Media`` inner class of the ``Menu`` instance.
    """
    if menu is None:
        menu = get_admin_menu(None)
    tpl = '<script type="text/javascript" src="%sadmin_tools/js/%s"></script>'
    return render_media('js', tpl, menu)
register.simple_tag(render_menu_js)


def render_menu_css(menu=None):
    """
    Template tag that renders the needed css files for the menu.
    It relies on the ``Media`` inner class of the ``Menu`` instance.
    """
    if menu is None:
        menu = get_admin_menu(None)
    tpl = '<link rel="stylesheet" type="text/css" media="%s" href="%sadmin_tools/css/%s" />'
    return render_media('css', tpl, menu)
register.simple_tag(render_menu_css)
