"""
django-admin-tools default dashboards.
"""

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.dashboard.models import *


class DefaultIndexDashboard(Dashboard):
    """
    Default admin index dashboard.
    """ 
    def __init__(self, *args, **kwargs):
        super(DefaultIndexDashboard, self).__init__(*args, **kwargs)

        # append a link list module for "quick links"
        self.append(LinkListDashboardModule(
            title=_('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            entries=[
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

        # append an app list module for "Applications"
        self.append(AppListDashboardModule(
            title=_('Applications'),
            exclude_list=('django.contrib',),
        ))

        # append an app list module for "Administration"
        self.append(AppListDashboardModule(
            title=_('Administration'),
            include_list=('django.contrib',),
        ))

        # append a recent actions module
        self.append(RecentActionsDashboardModule(
            enabled=False,
            title=_('Recent Actions'),
            limit=5
        ))

        # append a feed module
        self.append(FeedDashboardModule(
            enabled=False,
            title=_('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

        # append another link list module for "support". 
        self.append(LinkListDashboardModule(
            title=_('Support'),
            entries=[
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


class DefaultAppIndexDashboard(AppIndexDashboard):
    """
    Default admin app index dashboard.
    """
    def __init__(self, *args, **kwargs):
        super(DefaultAppIndexDashboard, self).__init__(*args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.append(ModelListDashboardModule(
            title=self.app_title,
            include_list=self.models,
        ))

        # append a recent actions module
        self.append(RecentActionsDashboardModule(
            title=_('Recent Actions'),
            include_list=self.models,
            limit=5
        ))
