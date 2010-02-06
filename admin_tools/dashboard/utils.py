"""
Dashboard utilities.
"""

from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils.importlib import import_module
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard.models import *
from admin_tools.dashboard.default_dashboard import *


def get_dashboard_from_context(context):
    try:
        request = context['request']
    except KeyError:
        request = HttpRequest()
    if request.META.get('REQUEST_URI') == reverse('admin:index'):
        return get_index_dashboard(request)
    try:
        app = context['app_list'][0]
        models = []
        app_label = app['name']
        for model, model_admin in admin.site._registry.items():
            if app['name'] == model._meta.app_label.title():
                app_label = model._meta.app_label
                for m in app['models']:
                    if m['name'] == capfirst(model._meta.verbose_name_plural):
                        mod = '%s.%s' % (model.__module__, model.__name__)
                        models.append(mod)
        return get_app_index_dashboard(request, app_label, models)
    except KeyError:
        return get_app_index_dashboard(request, '', [])


def get_index_dashboard(request):
    """
    Returns the admin dashboard defined by the user or the default one.
    """
    dashboard_cls = getattr(settings, 'ADMIN_TOOLS_INDEX_DASHBOARD', False)
    if dashboard_cls:
        mod, inst = dashboard_cls.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)()
    return DefaultIndexDashboard()


def get_app_index_dashboard(request, app_label='', model_list=[]):
    """
    Returns the admin dashboard defined by the user or the default one.
    """
    app_title = app_label.title()

    # try to discover corresponding app dashboard module
    mod_name = getattr(settings, 'ADMIN_TOOLS_APP_INDEX_DASHBOARD_MODULE', 'dashboard')
    mod_class = getattr(settings, 'ADMIN_TOOLS_APP_INDEX_DASHBOARD_CLASS', '%sDashboard' % capfirst(app_label))
    try:
        mod = import_module('%s.%s' % (app_label, mod_name))
        return getattr(mod, mod_class)(app_title, model_list)
    except:
        pass

    # try to discover a general app_index dashboard
    dashboard_cls = getattr(settings, 'ADMIN_TOOLS_APP_INDEX_DASHBOARD', False)
    if dashboard_cls:
        mod, inst = dashboard_cls.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)(app_title, model_list)

    # fallback to default dashboard
    return DefaultAppIndexDashboard(app_title, model_list)
