"""
Menu template tags, the following menu tags are available:

 * ``{% render_menu %}``
 * ``{% render_menu_item %}``
 * ``{% render_menu_css %}``

To load the menu tags in your templates: ``{% load menu_tags %}``.
"""

from django import template
from django.conf import settings
from django.http import HttpRequest
from admin_tools.menu.utils import get_admin_menu

register = template.Library()
tag_func = register.inclusion_tag('menu/dummy.html', takes_context=True)

def render_menu(context, menu=None):
    """
    Template tag that renders the menu, it takes an optional ``Menu`` instance
    as unique argument, if not given, the menu will be retrieved with the
    ``get_admin_menu`` function.
    """
    if menu is None:
        menu = get_admin_menu()

    menu.init_with_context(context)

    context.update({
        'template': menu.template,
        'menu': menu,
        'media_url': settings.MEDIA_URL.rstrip('/'),
    })
    return context
render_menu = tag_func(render_menu)


def render_menu_item(context, item, index=None):
    """
    Template tag that renders a given menu item, it takes a ``MenuItem``
    instance as unique parameter.
    """
    item.init_with_context(context)

    context.update({
        'template': item.template,
        'item': item,
        'index': index,
    })
    return context
render_menu_item = tag_func(render_menu_item)


def render_menu_css(context, menu=None):
    """
    Template tag that renders the menu css files,, it takes an optional 
    ``Menu`` instance as unique argument, if not given, the menu will be
    retrieved with the ``get_admin_menu`` function.
    """
    if menu is None:
        menu = get_admin_menu()

    context.update({
        'template': 'menu/css.html',
        'css_files': menu.Media.css,
        'media_url': settings.MEDIA_URL.rstrip('/'),
    })
    return context
render_menu_css = tag_func(render_menu_css)
