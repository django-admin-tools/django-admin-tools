from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from admin_tools.dashboard import Dashboard, AppIndexDashboard
from admin_tools.dashboard import modules


# to activate your index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_INDEX_DASHBOARD = 'test_proj.dashboard.CustomIndexDashboard'

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for test_proj.
    """
    class Media:
        css = {
            'all': ('test_app/dashboard.css',),
        }
        js = ('test_app/dashboard.js',)

    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'), reverse('admin:password_change')],
                [_('Log out'), reverse('admin:logout')],
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=['django.contrib.*'],
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        self.children.append(modules.ModelList(
            'Test1',
            ['django.contrib.auth.*', '*.Site', '*.Foo'],
            ['django.contrib.auth.models.User', 'test_app.*']
        ))

        # append a recent actions module
        self.children.append(
             modules.RecentActions(_('Recent Actions'), 5)
        )

        # append another link list module for "support".
        self.children.append(modules.LinkList(
            _('Support'),
            children=[
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
        self.children.append(modules.Group(
            title='Test group',
            children=[
                modules.ModelList(
                    'Tab 1',
                    ['django.contrib.*']
                ),
                modules.ModelList(
                    'Tab 2',
                    ['test_app.*']
                ),
            ]
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass


# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'test_proj.dashboard.CustomAppIndexDashboard'

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for test_proj.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(include_list=self.get_app_content_types()),
        ]

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
