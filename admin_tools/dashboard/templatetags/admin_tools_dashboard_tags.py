"""
Dashboard template tags, the following dashboard tags are available:
 * ``{% admin_tools_render_dashboard %}``
 * ``{% admin_tools_render_dashboard_module %}``
 * ``{% admin_tools_render_dashboard_css %}``

To load the dashboard tags: ``{% load admin_tools_dashboard_tags %}``.
"""

import math
from django import template
from admin_tools.utils import get_media_url
from admin_tools.dashboard.utils import get_dashboard
from admin_tools.dashboard.models import DashboardPreferences

register = template.Library()
tag_func = register.inclusion_tag('admin_tools/dashboard/dummy.html', takes_context=True)


def admin_tools_render_dashboard(context, location='index', dashboard=None):
    """
    Template tag that renders the dashboard, it takes two optional arguments:
    
    ``location``
        The location of the dashboard, it can be 'index' (for the admin index
        dashboard) or 'app_index' (for the app index dashboard), the default
        value is 'index'.

    ``dashboard``
        An instance of ``Dashboard``, if not given, the dashboard is retrieved
        with the ``get_index_dashboard`` or ``get_app_index_dashboard``
        functions, depending on the ``location`` argument.
    """
    if dashboard is None:
        dashboard = get_dashboard(context, location)

    dashboard.init_with_context(context)

    try:
        preferences = DashboardPreferences.objects.get(user=context['request'].user).data
    except DashboardPreferences.DoesNotExist:
        preferences = '{}'

    context.update({
        'template': dashboard.template,
        'dashboard': dashboard,
        'dashboard_preferences': preferences,
        'split_at': math.ceil(float(len(dashboard.children))/float(dashboard.columns)),
        'media_url': get_media_url(),
        'has_disabled_modules': len([m for m in dashboard.children \
                                if not m.enabled]) > 0,
    })
    return context
admin_tools_render_dashboard = tag_func(admin_tools_render_dashboard)


def admin_tools_render_dashboard_module(context, module, index=None, subindex=None):
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
        'subindex': subindex,
    })
    return context
admin_tools_render_dashboard_module = tag_func(admin_tools_render_dashboard_module)


def admin_tools_render_dashboard_css(context, location='index', dashboard=None):
    """
    Template tag that renders the dashboard css files, it takes two optional
    arguments:
    
    ``location``
        The location of the dashboard, it can be 'index' (for the admin index
        dashboard) or 'app_index' (for the app index dashboard), the default
        value is 'index'.

    ``dashboard``
        An instance of ``Dashboard``, if not given, the dashboard is retrieved
        with the ``get_index_dashboard`` or ``get_app_index_dashboard``
        functions, depending on the ``location`` argument.
    """
    if dashboard is None:
        dashboard = get_dashboard(context, location)

    context.update({
        'template' : 'admin_tools/dashboard/css.html',
        'css_files': dashboard.Media.css,
        'media_url': get_media_url(),
    })
    return context
admin_tools_render_dashboard_css = tag_func(admin_tools_render_dashboard_css)
