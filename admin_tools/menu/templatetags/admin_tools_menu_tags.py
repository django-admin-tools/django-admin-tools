"""
Menu template tags, the following menu tags are available:

 * ``{% admin_tools_render_menu %}``
 * ``{% admin_tools_render_menu_item %}``
 * ``{% admin_tools_render_menu_css %}``

To load the menu tags in your templates: ``{% load admin_tools_menu_tags %}``.
"""

from django import template
from django.core.urlresolvers import reverse

from admin_tools.utils import get_media_url, get_admin_site_name
from admin_tools.menu import items
from admin_tools.menu.models import Bookmark
from admin_tools.menu.utils import get_admin_menu

register = template.Library()
tag_func = register.inclusion_tag('admin_tools/menu/dummy.html', takes_context=True)

def admin_tools_render_menu(context, menu=None):
    """
    Template tag that renders the menu, it takes an optional ``Menu`` instance
    as unique argument, if not given, the menu will be retrieved with the
    ``get_admin_menu`` function.
    """
    if menu is None:
        menu = get_admin_menu()

    menu.init_with_context(context)
    has_bookmark_item = False
    bookmark = None
    if len([c for c in menu.children if isinstance(c, items.Bookmarks)]) > 0:
        has_bookmark_item = True
        url = context['request'].get_full_path()
        try:
            bookmark = Bookmark.objects.filter(user=context['request'].user, url=url)[0]
        except:
            pass

    context.update({
        'template': menu.template,
        'menu': menu,
        'media_url': get_media_url(),
        'has_bookmark_item': has_bookmark_item,
        'bookmark': bookmark,
        'admin_url': reverse('%s:index' % get_admin_site_name(context)),
    })
    return context
admin_tools_render_menu = tag_func(admin_tools_render_menu)


def admin_tools_render_menu_item(context, item, index=None):
    """
    Template tag that renders a given menu item, it takes a ``MenuItem``
    instance as unique parameter.
    """
    item.init_with_context(context)

    context.update({
        'template': item.template,
        'item': item,
        'index': index,
        'selected': item.is_selected(context['request']),
        'admin_url': reverse('%s:index' % get_admin_site_name(context)),
    })
    return context
admin_tools_render_menu_item = tag_func(admin_tools_render_menu_item)


def admin_tools_render_menu_css(context, menu=None):
    """
    Template tag that renders the menu css files,, it takes an optional 
    ``Menu`` instance as unique argument, if not given, the menu will be
    retrieved with the ``get_admin_menu`` function.
    """
    if menu is None:
        menu = get_admin_menu()

    context.update({
        'template': 'admin_tools/menu/css.html',
        'css_files': menu.Media.css,
        'media_url': get_media_url(),
    })
    return context
admin_tools_render_menu_css = tag_func(admin_tools_render_menu_css)
