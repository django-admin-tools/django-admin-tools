"""
Theming template tags.

To load the theming tags just do: ``{% load theming_tags %}``.
"""

import os.path
from django import template
from django.conf import settings

register = template.Library()

def render_theming_css():
    """
    Template tag that renders the needed css files for the theming app.
    """
    css = getattr(settings, 'ADMIN_TOOLS_THEMING_CSS', False)
    try:
        media_url = settings.STATIC_URL
    except AttributeError:
        media_url = settings.MEDIA_URL
    if css:
        css = os.path.join(media_url, css)
    else:
        css = os.path.join(
            getattr(settings, 'ADMIN_TOOLS_MEDIA_URL', media_url),
            'admin_tools',
            'css',
            'theming.css'
        )
    return '<link rel="stylesheet" type="text/css" media="screen" href="%s" />' % css
register.simple_tag(render_theming_css)
