"""
Dashboard utilities.
"""
import types

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.text import capfirst
from django.core.urlresolvers import reverse

from admin_tools.dashboard.registry import Registry
from admin_tools.utils import get_admin_site

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

def _get_dashboard_cls(dashboard_cls, context):
    if type(dashboard_cls) is types.DictType:
        curr_url = context.get('request').META['PATH_INFO']
        for key in dashboard_cls:
            admin_site_mod, admin_site_inst = key.rsplit('.', 1)
            admin_site_mod = import_module(admin_site_mod)
            admin_site = getattr(admin_site_mod, admin_site_inst)
            admin_url = reverse('%s:index' % admin_site.name)
            if curr_url.startswith(admin_url):
                mod, inst = dashboard_cls[key].rsplit('.', 1)
                mod = import_module(mod)
                return getattr(mod, inst)
    else:
        mod, inst = dashboard_cls.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)
    raise ValueError('Dashboard matching "%s" not found' % dashboard_cls)

def get_index_dashboard(context):
    """
    Returns the admin dashboard defined by the user or the default one.
    """
    return _get_dashboard_cls(getattr(
        settings,
        'ADMIN_TOOLS_INDEX_DASHBOARD',
        'admin_tools.dashboard.dashboards.DefaultIndexDashboard'
    ), context)()

def get_app_index_dashboard(context):
    """
    Returns the admin dashboard defined by the user or the default one.
    """
    # this is a mess, needs cleanup !
    app = context['app_list'][0]
    model_list = []
    app_label = None
    app_title = app['name']
    admin_site = get_admin_site(context=context)

    for model, model_admin in admin_site._registry.items():
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
    return _get_dashboard_cls(getattr(
        settings,
        'ADMIN_TOOLS_APP_INDEX_DASHBOARD',
        'admin_tools.dashboard.dashboards.DefaultAppIndexDashboard'
    ), context)(app_title, model_list)
