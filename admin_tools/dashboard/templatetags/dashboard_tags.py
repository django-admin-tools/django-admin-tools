"""
Dashboard template tags, the following dashboard tags are available:
 * ``{% render_dashboard %}``
 * ``{% render_dashboard_module %}``
 * ``{% render_dashboard_css %}``

To load the dashboard tags: ``{% load dashboard_tags %}``.
"""

import math
from django import template
from django.conf import settings
from admin_tools.dashboard.utils import get_dashboard_from_context

register = template.Library()
tag_func = register.inclusion_tag('dashboard/dummy.html', takes_context=True)


def render_dashboard(context, dashboard=None):
    """
    Template tag that renders the dashboard, it takes an optional ``Dashboard``
    instance as unique argument, if not given, the dashboard is retrieved with
    the ``get_dashboard_from_context`` function.
    """
    if not dashboard:
        dashboard = get_dashboard_from_context(context)
    dashboard.init_with_context(context)
    context.update({
        'template': dashboard.template,
        'dashboard': dashboard,
        'split_at': math.ceil(float(len(dashboard.children))/float(dashboard.columns)),
        'media_url': settings.MEDIA_URL.rstrip('/'),
        'has_disabled_modules': len([m for m in dashboard.children \
                                if not m.enabled]) > 0,
    })
    return context
render_dashboard = tag_func(render_dashboard)


def render_dashboard_module(context, module, index=None):
    """
    Template tag that renders a given dashboard module, it takes a
    ``DashboardModule`` instance as first parameter and an integer ``index`` as
    second parameter, that is the index of the module in the dashboard.
    """
    module.init_with_context(context)
    context.update({
        'template': module.template,
        'module': module,
        'index': index,
    })
    return context
render_dashboard_module = tag_func(render_dashboard_module)


def render_dashboard_css(context, dashboard=None):
    """
    Template tag that renders the dashboard css files.
    """
    if dashboard is None:
        dashboard = get_dashboard_from_context(context)

    context.update({
        'template' : 'dashboard/css.html',
        'css_files': dashboard.Media.css,
        'media_url': settings.MEDIA_URL.rstrip('/'),
    })
    return context
render_dashboard_css = tag_func(render_dashboard_css)
