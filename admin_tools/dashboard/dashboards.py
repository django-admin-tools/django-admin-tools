"""
Module where admin tools dashboard classes are defined.
"""

from django.template.defaultfilters import slugify
try:
    from importlib import import_module
except ImportError:
    # Django < 1.9 and Python < 2.7
    from django.utils.importlib import import_module
from django.utils.translation import ugettext_lazy as _
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.utils.encoding import force_text

from admin_tools.dashboard import modules
from admin_tools.utils import get_admin_site_name, uniquify


class Dashboard(object):
    """
    Base class for dashboards.
    The Dashboard class is a simple python list that has three additional
    properties:

    ``title``
        The dashboard title, by default, it is displayed above the dashboard
        in a ``h2`` tag. Default value: 'Dashboard'.

    ``template``
        The template to use to render the dashboard.
        Default value: 'admin_tools/dashboard/dashboard.html'

    ``columns``
        An integer that represents the number of columns for the dashboard.
        Default value: 2.

    If you want to customize the look of your dashboard and it's modules, you
    can declare css stylesheets and/or javascript files to include when
    rendering the dashboard (these files should be placed in your
    media path), for example::

        from admin_tools.dashboard import Dashboard

        class MyDashboard(Dashboard):
            class Media:
                css = {
                    'screen, projection': ('css/mydashboard.css',),
                }
                js = ('js/mydashboard.js',)

    Here's an example of a custom dashboard::

        from django.core.urlresolvers import reverse
        from django.utils.translation import ugettext_lazy as _
        from admin_tools.dashboard import modules, Dashboard

        class MyDashboard(Dashboard):

            # we want a 3 columns layout
            columns = 3

            def __init__(self, **kwargs):

                # append an app list module for "Applications"
                self.children.append(modules.AppList(
                    title=_('Applications'),
                    exclude=('django.contrib.*',),
                ))

                # append an app list module for "Administration"
                self.children.append(modules.AppList(
                    title=_('Administration'),
                    models=('django.contrib.*',),
                ))

                # append a recent actions module
                self.children.append(modules.RecentActions(
                    title=_('Recent Actions'),
                    limit=5
                ))

    Below is a screenshot of the resulting dashboard:

    .. image:: images/dashboard_example.png
    """

    title = _('Dashboard')
    template = 'admin_tools/dashboard/dashboard.html'
    columns = 2
    children = None

    class Media:
        css = ()
        js = ()

    def __init__(self, **kwargs):
        for key in kwargs:
            if hasattr(self.__class__, key):
                setattr(self, key, kwargs[key])
        self.children = self.children or []

    def init_with_context(self, context):
        """
        Sometimes you may need to access context or request variables to build
        your dashboard, this is what the ``init_with_context()`` method is for.
        This method is called just before the display with a
        ``django.template.RequestContext`` as unique argument, so you can
        access to all context variables and to the ``django.http.HttpRequest``.
        """
        pass

    def get_id(self):
        """
        Internal method used to distinguish different dashboards in js code.
        """
        return 'dashboard'

    def _prepare_children(self):
        """ Enumerates children without explicit id """
        seen = set()
        for id, module in enumerate(self.children):
            module.id = uniquify(module.id or str(id+1), seen)
            module._prepare_children()


class AppIndexDashboard(Dashboard):
    """
    Class that represents an app index dashboard, app index dashboards are
    displayed in the applications index page.
    :class:`~admin_tools.dashboard.AppIndexDashboard` is very similar to the
    :class:`~admin_tools.dashboard.Dashboard` class except
    that its constructor receives two extra arguments:

    ``app_title``
        The title of the application

    ``models``
        A list of strings representing the available models for the current
        application, example::

            ['yourproject.app.Model1', 'yourproject.app.Model2']

    It also provides two helper methods:

    ``get_app_model_classes()``
        Method that returns the list of model classes for the current app.

    ``get_app_content_types()``
        Method that returns the list of content types for the current app.

    If you want to provide custom app index dashboard, be sure to inherit from
    this class instead of the :class:`~admin_tools.dashboard.Dashboard` class.

    Here's an example of a custom app index dashboard::

        from django.core.urlresolvers import reverse
        from django.utils.translation import ugettext_lazy as _
        from admin_tools.dashboard import modules, AppIndexDashboard

        class MyAppIndexDashboard(AppIndexDashboard):

            # we don't want a title, it's redundant
            title = ''

            def __init__(self, app_title, models, **kwargs):
                AppIndexDashboard.__init__(self, app_title, models, **kwargs)

                # append a model list module that lists all models
                # for the app and a recent actions module for the current app
                self.children += [
                    modules.ModelList(self.app_title, self.models),
                    modules.RecentActions(
                        include_list=self.models,
                        limit=5
                    )
                ]

    Below is a screenshot of the resulting dashboard:

    .. image:: images/dashboard_app_index_example.png
    """

    models = None
    app_title = None

    def __init__(self, app_title, models, **kwargs):
        kwargs.update({'app_title': app_title, 'models': models})
        super(AppIndexDashboard, self).__init__(**kwargs)

    def get_app_model_classes(self):
        """
        Helper method that returns a list of model classes for the current app.
        """
        models = []
        for m in self.models:
            mod, cls = m.rsplit('.', 1)
            mod = import_module(mod)
            models.append(getattr(mod, cls))
        return models

    def get_app_content_types(self):
        """
        Return a list of all content_types for this app.
        """
        # Import this here to silence RemovedInDjango19Warning. See #15
        from django.contrib.contenttypes.models import ContentType

        return [ContentType.objects.get_for_model(c) for c
                in self.get_app_model_classes()]

    def get_id(self):
        """
        Internal method used to distinguish different dashboards in js code.
        """
        return '%s-dashboard' % slugify(force_text(self.app_title))


class DefaultIndexDashboard(Dashboard):
    """
    The default dashboard displayed on the admin index page.
    To change the default dashboard you'll have to type the following from the
    commandline in your project root directory::

        python manage.py customdashboard

    And then set the ``ADMIN_TOOLS_INDEX_DASHBOARD`` settings variable to
    point to your custom index dashboard class.
    """
    def init_with_context(self, context):
        site_name = get_admin_site_name(context)
        # append a link list module for "quick links"
        self.children.append(modules.LinkList(
            _('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                [_('Return to site'), '/'],
                [_('Change password'),
                 reverse('%s:password_change' % site_name)],
                [_('Log out'), reverse('%s:logout' % site_name)],
            ]
        ))

        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            _('Applications'),
            exclude=('django.contrib.*',),
        ))

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            _('Administration'),
            models=('django.contrib.*',),
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(_('Recent Actions'), 5))

        # append a feed module
        self.children.append(modules.Feed(
            _('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

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


class DefaultAppIndexDashboard(AppIndexDashboard):
    """
    The default dashboard displayed on the applications index page.
    To change the default dashboard you'll have to type the following from the
    commandline in your project root directory::

        python manage.py customdashboard

    And then set the ``ADMIN_TOOLS_APP_INDEX_DASHBOARD`` settings variable to
    point to your custom app index dashboard class.
    """

    # we disable title because its redundant with the model list module
    title = ''

    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # append a model list module and a recent actions module
        self.children += [
            modules.ModelList(self.app_title, self.models),
            modules.RecentActions(
                _('Recent Actions'),
                include_list=self.get_app_content_types(),
                limit=5
            )
        ]
