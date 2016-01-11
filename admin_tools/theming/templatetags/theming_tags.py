"""
Theming template tags.

To load the theming tags just do: ``{% load theming_tags %}``.
"""

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe

register = template.Library()


def render_theming_css():
    """
    Template tag that renders the needed css files for the theming app.
    """
    css = getattr(settings, 'ADMIN_TOOLS_THEMING_CSS', False)
    if not css:
        css = '/'.join(['admin_tools', 'css', 'theming.css'])
    return mark_safe(
        '<link rel="stylesheet" type="text/css" media="screen" href="%s" />' %
        staticfiles_storage.url(css)
    )
register.simple_tag(render_theming_css)
