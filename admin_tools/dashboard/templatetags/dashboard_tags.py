"""
Dashboard template tags, the following dashboard tags are available:
* ``{% render_dashboard %}``
* ``{% render_dashboard_module %}``
* ``{% render_dashboard_js %}``
* ``{% render_dashboard_css %}``

To load the dashboard tags just do: ``{% load dashboard_tags %}``.
"""

import math
from django import template
from admin_tools.utils import render_media
from admin_tools.dashboard.utils import get_dashboard_from_context

register = template.Library()


def render_dashboard(context, dashboard=None):
    """
    Template tag that renders the dashboard, it takes an optional ``Dashboard``
    instance as unique argument, if not given, the dashboard is retrieved with
    the ``get_dashboard_from_context`` function.
    """
    if not dashboard:
        dashboard = get_dashboard_from_context(context)
    context.update({
        'template': dashboard.template,
        'dashboard': dashboard,
        'split_at': math.ceil(float(len(dashboard))/float(dashboard.columns))
    })
    return context
render_dashboard = register.inclusion_tag(
    'dashboard/dummy.html',
    takes_context=True
)(render_dashboard)


def render_dashboard_module(context, module, index=None):
    """
    Template tag that renders a given dashboard module, it takes a
    ``DashboardModule`` instance as first parameter and an integer ``index`` as
    second parameter, that is the index of the module in the dashboard.
    """
    module.render(context['request'])
    context.update({
        'template': module.template,
        'module': module,
        'index': index,
    })
    return context
render_dashboard_module = register.inclusion_tag(
    'dashboard/dummy.html',
    takes_context=True
)(render_dashboard_module)


def render_dashboard_js(dashboard=None):
    """
    Template tag that renders the needed js files for the dashboard.
    It relies on the ``Media`` inner class of the ``Dashboard`` instance.
    """
    if dashboard is None:
        dashboard = get_dashboard_from_context({})
    tpl = '<script type="text/javascript" src="%sadmin_tools/js/%s"></script>'
    return render_media('js', tpl, dashboard)
register.simple_tag(render_dashboard_js)


def render_dashboard_css(dashboard=None):
    """
    Template tag that renders the needed css files for the dashboard.
    It relies on the ``Media`` inner class of the ``Dashboard`` instance.
    """
    if dashboard is None:
        dashboard = get_dashboard_from_context({})
    tpl = '<link rel="stylesheet" type="text/css" media="%s" href="%sadmin_tools/css/%s" />'
    return render_media('css', tpl, dashboard)
register.simple_tag(render_dashboard_css)
