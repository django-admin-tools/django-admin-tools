"""
Dashboard utilities.
"""

from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard.models import *


def get_dashboard_from_context(context):
    try:
        request = context['request']
    except KeyError:
        request = HttpRequest()
    if request.META.get('REQUEST_URI') == reverse('admin:index'):
        return get_index_dashboard(request)
    try:
        app = context['app_list'][0]
        model_list = []
        for model, model_admin in admin.site._registry.items():
            if app['name'] == model._meta.app_label.title():
                for m in app['models']:
                    if m['name'] == capfirst(model._meta.verbose_name_plural):
                        mod = '%s.%s' % (model.__module__, model.__name__)
                        model_list.append(mod)
        return get_app_index_dashboard(request, app['name'], model_list)
    except KeyError:
        return get_app_index_dashboard(request)


def get_index_dashboard(request):
    """
    Returns the admin dashboard defined by the user or the default one.
    """
    provider = getattr(settings, 'ADMIN_TOOLS_INDEX_DASHBOARD_PROVIDER', False)
    if provider:
        from django.utils.importlib import import_module
        mod, inst = provider.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)()

    index_dashboard = Dashboard()
    index_dashboard.append(LinkListDashboardModule(
        title=_('Quick links'),
        layout='inline',
        draggable=False,
        deletable=False,
        collapsible=False,
        link_list=[
            {
                'title': _('Return to site'),
                'url': '/',
            },
            {
                'title': _('Change password'),
                'url': reverse('admin:password_change'),
            },
            {
                'title': _('Log out'),
                'url': reverse('admin:logout')
            },
        ]
    ))
    index_dashboard.append(AppListDashboardModule(
        title=_('Applications'),
        exclude_list=('django.contrib',),
    ))
    index_dashboard.append(AppListDashboardModule(
        title=_('Administration'),
        include_list=('django.contrib',),
    ))
    index_dashboard.append(RecentActionsDashboardModule(
        enabled=False,
        title=_('Recent Actions'),
        limit=5
    ))
    index_dashboard.append(FeedDashboardModule(
        enabled=False,
        title=_('Latest Django News'),
        feed_url='http://www.djangoproject.com/rss/weblog/',
        limit=5
    ))
    index_dashboard.append(LinkListDashboardModule(
        title=_('Support'),
        link_list=[
            {
                'title': _('Django documentation'),
                'url': 'http://docs.djangoproject.com/',
                'external': True,
            },
            {
                'title': _('Django "django-users" mailing list'),
                'url': 'http://groups.google.com/group/django-users',
                'external': True,
            },
            {
                'title': _('Django irc channel'),
                'url': 'irc://irc.freenode.net/django',
                'external': True,
            },
        ]
    ))
    return index_dashboard


def get_app_index_dashboard(request, app_title='', model_list=[]):
    """
    Returns the admin dashboard defined by the user or the default one.
    """
    provider = getattr(settings, 'ADMIN_TOOLS_APP_INDEX_DASHBOARD_PROVIDER', False)
    if provider:
        from django.utils.importlib import import_module
        mod, inst = provider.rsplit('.', 1)
        mod = import_module(mod)
        return getattr(mod, inst)(app_name)

    import logging
    logging.warn(model_list)
    app_index_dashboard = Dashboard(title='')
    app_index_dashboard.append(ModelListDashboardModule(
        title=app_title,
        include_list=model_list,
    ))
    app_index_dashboard.append(RecentActionsDashboardModule(
        title=_('Recent Actions'),
        include_list=model_list,
        limit=5
    ))
    return app_index_dashboard
