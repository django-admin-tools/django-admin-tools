"""
Menu template tags, the following menu tags are available:
* ``{% render_menu %}``
* ``{% render_menu_item %}``

To load the menu tags just do: ``{% load menu_tags %}``.
"""

from django import template
from django.conf import settings
from django.http import HttpRequest
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

    menu.render(context['request'])
    context.update({
        'template': menu.template,
        'menu': menu,
        'media_url': settings.MEDIA_URL.rstrip('/'),
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


def render_menu_css(context, menu=None):
    """
    Template tag that renders the menu css files.
    """
    if menu is None:
        menu = get_admin_menu(context['request'])

    context.update({
        'css_files': menu.Media.css,
        'media_url': settings.MEDIA_URL.rstrip('/'),
    })
    return context
render_menu_css = register.inclusion_tag(
    'menu/css.html',
    takes_context=True
)(render_menu_css)
