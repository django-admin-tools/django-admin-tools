"""
Dashboard utilities.
"""
from django.conf import settings
from django.contrib import admin
from django.utils.importlib import import_module
from django.utils.text import capfirst
from admin_tools.dashboard.registry import Registry

def get_dashboard(context, location):
    """
    Returns the dashboard that match the given ``location``
    (index or app_index).
    """
    if location == 'index':
        return get_index_dashboard(context)
    elif location == 'app_index':
        return get_app_index_dashboard(context)
    raise ValueError('Invalid dashboard location: "%s"' % location)


def get_index_dashboard(context):
    """
    Returns the admin dashboard defined by the user or the default one.
    """
    dashboard_cls = getattr(
        settings,
        'ADMIN_TOOLS_INDEX_DASHBOARD',
        'admin_tools.dashboard.dashboards.DefaultIndexDashboard'
    )
    mod, inst = dashboard_cls.rsplit('.', 1)
    mod = import_module(mod)
    return getattr(mod, inst)()


def get_app_index_dashboard(context):
    """
    Returns the admin dashboard defined by the user or the default one.
    """
    # this is a mess, needs cleanup !
    app = context['app_list'][0]
    model_list = []
    app_label = None
    app_title = app['name']
    for model, model_admin in admin.site._registry.items():
        if app['name'] == model._meta.app_label.title():
            split = model.__module__.find(model._meta.app_label)
            app_label = model.__module__[0:split] + model._meta.app_label
            app_title = model._meta.app_label.title()
            for m in app['models']:
                if m['name'] == capfirst(model._meta.verbose_name_plural):
                    mod = '%s.%s' % (model.__module__, model.__name__)
                    model_list.append(mod)

    # if an app has registered its own dashboard, use it
    if app_label is not None and app_label in Registry.registry:
        return Registry.registry[app_label](app_title, model_list)

    # try to discover a general app_index dashboard (with fallback to the
    # default dashboard)
    dashboard_cls = getattr(
        settings,
        'ADMIN_TOOLS_APP_INDEX_DASHBOARD',
        'admin_tools.dashboard.dashboards.DefaultAppIndexDashboard'
    )
    mod, inst = dashboard_cls.rsplit('.', 1)
    mod = import_module(mod)
    return getattr(mod, inst)(app_title, model_list)
