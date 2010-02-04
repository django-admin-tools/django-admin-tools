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
    if css:
        css = os.path.join(settings.MEDIA_URL, css)
    else:
        css = os.path.join(
            getattr(settings, 'ADMIN_TOOLS_MEDIA_URL', settings.MEDIA_URL),
            'admin_tools',
            'css',
            'theming.css'
        )
    return '<link rel="stylesheet" type="text/css" media="screen" href="%s" />' % css
register.simple_tag(render_theming_css)
