"""
Theming template tags.

To load the theming tags just do: ``{% load theming_tags %}``.
"""

from django import template
from django.conf import settings
from admin_tools.utils import get_media_url

register = template.Library()

def render_theming_css():
    """
    Template tag that renders the needed css files for the theming app.
    """
    css = getattr(settings, 'ADMIN_TOOLS_THEMING_CSS', False)
    if css:
        css = '/'.join([get_media_url(), css])
    else:
        css = '/'.join([get_media_url(), 'admin_tools', 'css', 'theming.css'])
    return '<link rel="stylesheet" type="text/css" media="screen" href="%s" />' % css
register.simple_tag(render_theming_css)
