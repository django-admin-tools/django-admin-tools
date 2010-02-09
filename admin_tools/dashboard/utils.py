"""
Dashboard utilities.
"""

from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils.importlib import import_module
from django.utils.text import capfirst
from admin_tools.dashboard import Registry
from admin_tools.dashboard.models import *



def get_dashboard_from_context(context):
    """
    Return the dashboard instance given the context.
    """
    request = context['request']
    if request.META.get('REQUEST_URI') == reverse('admin:index'):
        return get_index_dashboard()
    # this is a mess, needs cleanup !
    app = context['app_list'][0]
    models = []
    app_label = None
    app_title = app['name']
    for model, model_admin in admin.site._registry.items():
        if app['name'] == model._meta.app_label.title():
            split = model.__module__.find(model._meta.app_label)
            app_label = model.__module__[0:split] + model._meta.app_label
            app_title = model._meta.app_label.title
            for m in app['models']:
                if m['name'] == capfirst(model._meta.verbose_name_plural):
                    mod = '%s.%s' % (model.__module__, model.__name__)
                    models.append(mod)
    return get_app_index_dashboard(app_label, app_title, models)


def get_index_dashboard():
    """
    Returns the admin dashboard defined by the user or the default one.
    """
    dashboard_cls = getattr(
        settings,
        'ADMIN_TOOLS_INDEX_DASHBOARD',
        'admin_tools.dashboard.models.DefaultIndexDashboard'
    )
    try:
        mod, inst = dashboard_cls.rsplit('.', 1)
        mod = import_module(mod)
    except:
        raise ImproperlyConfigured((
            'The class pointed by your ADMIN_TOOLS_INDEX_DASHBOARD '
            'setting variable cannot be imported'
        ))
    return getattr(mod, inst)()


def get_app_index_dashboard(app_label=None, app_title='', model_list=[]):
    """
    Returns the admin dashboard defined by the user or the default one.
    """

    # if an app has registered its own dashboard, use it
    if app_label is not None and app_label in Registry.registry:
        return Registry.registry[app_label](app_title, model_list)

    # try to discover a general app_index dashboard (with fallback to the 
    # default dashboard)
    dashboard_cls = getattr(
        settings,
        'ADMIN_TOOLS_APP_INDEX_DASHBOARD',
        'admin_tools.dashboard.models.DefaultAppIndexDashboard'
    )
    try:
        mod, inst = dashboard_cls.rsplit('.', 1)
        mod = import_module(mod)
    except:
        raise ImproperlyConfigured((
            'The class pointed by your ADMIN_TOOLS_APP_INDEX_DASHBOARD '
            'setting variable cannot be imported'
        ))
    return getattr(mod, inst)(app_title, model_list)
