"""
This module contains the base classes for the dashboard and dashboard modules.
"""

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from admin_tools.utils import AppListElementMixin


class Dashboard(list):
    """
    Base class for dashboards.
    The Dashboard class is a simple python list that has three additional
    properties:

    ``title``
        The dashboard title, by default, it is displayed above the dashboard
        in a ``h2`` tag. Default value: 'Dashboard'.

    ``template``
        The template to use to render the dashboard.
        Default value: 'dashboard/dashboard.html'

    ``columns``
        An integer that represents the number of columns for the dashboard.
        Default value: 2.

    If you want to customize the look of your dashboard and it's modules, you
    can declare css stylesheets and/or javascript files to include when 
    rendering the dashboard, for example::

        from admin_tools.dashboard.models import *

        class MyDashboard(Dashboard):
            class Media:
                css = {'screen': '/media/css/mydashboard.css'}
                js = ('/media/js/mydashboard.js',)

    Here's an example of a custom dashboard::

        from django.core.urlresolvers import reverse
        from django.utils.translation import ugettext_lazy as _
        from admin_tools.dashboard.models import *

        class MyDashboard(Dashboard):
            def render(self, request):
                # we want a 3 columns layout
                self.columns = 3

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

    Below is a screenshot of the resulting dashboard:

    .. image:: images/dashboard_example.png
    """
    class Media:
        css = {
            'all': 'dashboard.css',
            'ie': 'dashboard-ie.css',
        }
        js  = (
            'jquery/jquery-1.4.1.min.js',
            'jquery/jquery-ui-1.8rc1.custom.min.js',
            'jquery/jquery.cookie.min.js',
            'json.min.js',
            'jquery/jquery.dashboard.js',
        )

    def __init__(self, *args, **kwargs):
        """
        Dashboard constructor.
        """
        super(Dashboard, self).__init__()
        self.title = kwargs.get('title', _('Dashboard'))
        self.template = kwargs.get('template', 'dashboard/dashboard.html')
        self.columns = kwargs.get('columns', 2)

    def render(self, request):
        """
        The ``Dashboard.render()`` method is called just before the display
        with a ``django.http.HttpRequest`` as unique argument.
        Override this method to build your dashboard if you need to access to
        the request instance.
        """
        pass


class AppIndexDashboard(Dashboard):
    """
    Class that represents an app index dashboard, app index dashboards are 
    displayed in the applications index page.
    ``AppIndexDashboard`` is very similar to the ``Dashboard`` class except
    that its constructor receives two extra arguments:

    ``app_title``
        The title of the application

    ``models``
        A list of strings representing the available models for the current 
        application, example::
            
            ['yourproject.app.Model1', 'yourproject.app.Model2']

    If you want to provide custom app index dashboard, be sure to inherit from
    this class instead of the ``Dashboard`` class.

    Here's an example of a custom app index dashboard::

        from django.core.urlresolvers import reverse
        from django.utils.translation import ugettext_lazy as _
        from admin_tools.dashboard.models import *

        class MyAppIndexDashboard(AppIndexDashboard):
            def render(self, request):
                # we don't want a title, it's redundant
                self.title = ''

                # append a model list module that lists all models 
                # for the app
                self.append(ModelListDashboardModule(
                    title=self.app_title,
                    include_list=self.models,
                ))
        
                # append a recent actions module for the current app
                self.append(RecentActionsDashboardModule(
                    title=_('Recent Actions'),
                    include_list=self.models,
                    limit=5
                ))

    Below is a screenshot of the resulting dashboard:

    .. image:: images/dashboard_app_index_example.png
    """
    def __init__(self, app_title, models, *args, **kwargs):
        super(AppIndexDashboard, self).__init__(*args, **kwargs)
        self.app_title = app_title
        self.models = models


class DashboardModule(object):
    """
    Base class for all dashboard modules.
    Dashboard modules have the following properties:

    ``enabled``
        Boolean that determines whether the module should be enabled in 
        the dashboard by default or not. Default value: ``True``.

    ``draggable``
        Boolean that determines whether the module can be draggable or not.
        Draggable modules can be re-arranged by users. Default value: ``True``.

    ``collapsible``
        Boolean that determines whether the module is collapsible, this 
        allows users to show/hide module content. Default: ``True``.

    ``deletable``
        Boolean that determines whether the module can be removed from the 
        dashboard by users or not. Default: ``True``.

    ``title``
        String that contains the module title, make sure you use the django
        gettext functions if your application is multilingual. 
        Default value: ''.

    ``title_url``
        String that contains the module title URL. If given the module 
        title will be a link to this URL. Default value: ``None``.

    ``css_classes``
        A list of css classes to be added to the module ``div`` class 
        attribute. Default value: ``None``.

    ``pre_content``
        Text or HTML content to display above the module content.
        Default value: ``None``.

    ``content``
        The module text or HTML content. Default value: ``None``.

    ``post_content``
        Text or HTML content to display under the module content.
        Default value: ``None``.

    ``template``
        The template to use to render the module.
        Default value: 'dashboard/module.html'.
    """
    def __init__(self, *args, **kwargs):
        self.enabled = kwargs.get('enabled', True)
        self.draggable = kwargs.get('draggable', True)
        self.collapsible = kwargs.get('collapsible', True)
        self.deletable = kwargs.get('deletable', True)
        self.title = kwargs.get('title', '')
        self.title_url = kwargs.get('title_url', None)
        self.css_classes = kwargs.get('css_classes', [])
        self.pre_content = kwargs.get('pre_content')
        self.post_content = kwargs.get('post_content')
        self.template = kwargs.get('template', 'dashboard/module.html')
        self.entries = kwargs.get('entries', [])

    def render(self, request):
        pass

    def is_empty(self):
        """
        Return True if the module has no content and False otherwise.

        >>> mod = DashboardModule()
        >>> mod.is_empty()
        True
        >>> mod.pre_content = 'foo'
        >>> mod.is_empty()
        False
        >>> mod.pre_content = None
        >>> mod.is_empty()
        True
        >>> mod.entries.append('foo')
        >>> mod.is_empty()
        False
        >>> mod.entries = []
        >>> mod.is_empty()
        True
        """
        return self.pre_content is None and \
               self.post_content is None and \
               len(self.entries) == 0

    def render_css_classes(self):
        """
        Return a string containing the css classes for the module.

        >>> mod = DashboardModule(enabled=False, draggable=True, 
        ...                       collapsible=True, deletable=True)
        >>> mod.render_css_classes()
        'dashboard-module disabled draggable collapsible deletable'
        >>> mod.css_classes.append('foo')
        >>> mod.render_css_classes()
        'dashboard-module disabled draggable collapsible deletable foo'
        >>> mod.enabled = True
        >>> mod.render_css_classes()
        'dashboard-module draggable collapsible deletable foo'
        """
        ret = ['dashboard-module']
        if not self.enabled:
            ret.append('disabled')
        if self.draggable:
            ret.append('draggable')
        if self.collapsible:
            ret.append('collapsible')
        if self.deletable:
            ret.append('deletable')
        ret += self.css_classes
        return ' '.join(ret)


class LinkListDashboardModule(DashboardModule):
    """
    A module that displays a list of links.
    As well as the ``DashboardModule`` properties, the
    ``LinkListDashboardModule`` takes an extra keyword argument:

    ``layout``
        The layout of the list, possible values are ``stacked`` and ``inline``.
        The default value is ``stacked``.

    Link list modules entries are simple python dictionaries that can have the
    following keys:

    ``title``
        The link title.

    ``url``
        The link URL.

    ``external``
        Boolean that indicates whether the link is an external one or not.

    ``description``
        A string describing the link, it will be the ``title`` attribute of
        the html ``a`` tag.

    Here's a small example of building a link list module::
        
        from admin_tools.dashboard.models import *
        
        mydashboard = Dashboard()
        mydashboard.append(LinkListDashboardModule(
            layout='inline',
            entries=(
                {
                    'title': 'Python website',
                    'url': 'http://www.python.org',
                    'external': True,
                    'title': 'Python programming language rocks !',
                },
                {
                    'title': 'Django website',
                    'url': 'http://www.djangoproject.com',
                    'external': True
                },
                {
                    'title': 'Some internal link',
                    'url': '/some/internal/link/',
                    'external': False
                },
            )
        ))

    The screenshot of what this code produces:

    .. image:: images/linklist_dashboard_module.png
    """

    def __init__(self, *args, **kwargs):
        super(LinkListDashboardModule, self).__init__(*args, **kwargs)
        self.title = kwargs.get('title', _('Links'))
        self.template = kwargs.get('template',
                                   'dashboard/modules/link_list.html')
        self.layout = kwargs.get('layout', 'stacked')


class AppListDashboardModule(DashboardModule, AppListElementMixin):
    """
    Module that lists installed apps and their models.
    As well as the ``DashboardModule`` properties, the
    ``AppListDashboardModule`` has two extra properties:

    ``exclude_list``
        A list of apps to exclude, if an app name (e.g. "django.contrib.auth"
        starts with an element of this list (e.g. "django.contrib") it won't
        appear in the dashboard module.

    ``include_list``
        A list of apps to include, only apps whose name (e.g. 
        "django.contrib.auth") starts with one of the strings (e.g. 
        "django.contrib") in the list will appear in the dashboard module.

    If no include/exclude list is provided, **all apps** are shown.

    Here's a small example of building an app list module::
 
        from admin_tools.dashboard.models import *
     
        mydashboard = Dashboard()

        # will only list the django.contrib apps
        mydashboard.append(AppListDashboardModule(
            title='Administration',
            include_list=('django.contrib',)
        )) 
        # will list all apps except the django.contrib ones
        mydashboard.append(AppListDashboardModule(
            title='Applications',
            exclude_list=('django.contrib',)
        )) 

    The screenshot of what this code produces:

    .. image:: images/applist_dashboard_module.png

    .. note::

        Note that this module takes into account user permissions, for 
        example, if a user has no rights to change or add a ``Group``, then
        the django.contrib.auth.Group model line will not be displayed.
    """

    def __init__(self, *args, **kwargs):
        super(AppListDashboardModule, self).__init__(*args, **kwargs)
        self.title = kwargs.get('title', _('Applications'))
        self.template = kwargs.get('template',
                                   'dashboard/modules/app_list.html')
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])

    def render(self, request):
        apps = {}
        for model, model_admin in admin.site._registry.items():
            perms = self._check_perms(request, model, model_admin)
            if not perms or ('add' not in perms and 'change' not in perms):
                continue
            app_label = model._meta.app_label
            if app_label not in apps:
                apps[app_label] = {
                    'title': capfirst(app_label.title()),
                    'url': reverse('admin:app_list', args=(app_label,)),
                    'models': []
                }
            model_dict = {}
            model_dict['title'] = capfirst(model._meta.verbose_name_plural)
            if perms['change']:
                model_dict['change_url'] = self._get_admin_change_url(model)
            if perms['add']:
                model_dict['add_url'] = self._get_admin_add_url(model)
            apps[app_label]['models'].append(model_dict)

        apps_sorted = apps.keys()
        apps_sorted.sort()
        for app in apps_sorted:
            # sort model list alphabetically
            apps[app]['models'].sort(lambda x, y: cmp(x['title'], y['title']))
            self.entries.append(apps[app])


class ModelListDashboardModule(DashboardModule, AppListElementMixin):
    """
    Module that lists a set of models.
    As well as the ``DashboardModule`` properties, the
    ``ModelListDashboardModule`` takes two extra keyword arguments:

    ``include_list``
        A list of models to include, only models whose name (e.g. 
        "blog.comments.Comment") starts with one of the strings (e.g. "blog") 
        in the include list will appear in the dashboard module.

    ``exclude_list``
        A list of models to exclude, if a model name (e.g. 
        "blog.comments.Comment" starts with an element of this list (e.g. 
        "blog.comments") it won't appear in the dashboard module.

    Here's a small example of building a model list module::
        
        from admin_tools.dashboard.models import *
        
        mydashboard = Dashboard()
        # will only list the django.contrib.auth models
        mydashboard.append(ModelListDashboardModule(
            title='Authentication',
            include_list=('django.contrib.auth',)
        )) 

    The screenshot of what this code produces:

    .. image:: images/recentactions_dashboard_module.png

    .. note::

        Note that this module takes into account user permissions, for 
        example, if a user has no rights to change or add a ``Group``, then
        the django.contrib.auth.Group model line will not be displayed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelListDashboardModule, self).__init__(*args, **kwargs)
        self.title = kwargs.get('title', '')
        self.template = kwargs.get('template',
                                   'dashboard/modules/model_list.html')
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])

    def render(self, request):
        for model, model_admin in admin.site._registry.items():
            perms = self._check_perms(request, model, model_admin)
            if not perms:
                continue
            model_dict = {}
            model_dict['title'] = capfirst(model._meta.verbose_name_plural)
            if perms['change']:
                model_dict['change_url'] = self._get_admin_change_url(model)
            if perms['add']:
                model_dict['add_url'] = self._get_admin_add_url(model)
            self.entries.append(model_dict)

        # sort model list alphabetically
        self.entries.sort(lambda x, y: cmp(x['title'], y['title']))


class RecentActionsDashboardModule(DashboardModule):
    """
    Module that lists the recent actions for the current user.
    As well as the ``DashboardModule`` properties, the
    ``RecentActionsDashboardModule`` takes three extra keyword arguments:

    ``include_list``
        A list of models to include, only actions for models whose name (e.g. 
        "blog.comments.Comment") starts with one of the strings (e.g. "blog") 
        in the include list will appear in the dashboard module.

    ``exclude_list``
        A list of models to exclude, if a model name (e.g. 
        "blog.comments.Comment" starts with an element of this list (e.g. 
        "blog.comments") it's recent actions won't appear in the dashboard
        module.

    ``limit``
        The maximum number of entries to display. Default value: 10.

    Here's a small example of building a recent actions module::
        
        from admin_tools.dashboard.models import *
        
        mydashboard = Dashboard()
        # will only list the django.contrib apps
        mydashboard.append(RecentActionsDashboardModule(
            title='Django CMS recent actions',
            include_list=('cms',)
        ))

    The screenshot of what this code produces:

    .. image:: images/recentactions_dashboard_module.png
    """

    def __init__(self, *args, **kwargs):
        super(RecentActionsDashboardModule, self).__init__(*args, **kwargs)
        self.title = kwargs.get('title', _('Recent Actions'))
        self.template = kwargs.get('template',
                                   'dashboard/modules/recent_actions.html')
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])
        self.limit = kwargs.get('limit', 10)

    def render(self, request):
        from django.contrib.admin.models import LogEntry
        if request.user is None:
            qs = LogEntry.objects.all()
        else:
            qs = LogEntry.objects.filter(user__id__exact=request.user.id)
        # todo: RecentActionsDashboardModule: filter by contenttype
        if self.include_list:
            pass
        if self.exclude_list:
            pass
        self.entries = qs.select_related('content_type', 'user')[:self.limit]


class FeedDashboardModule(DashboardModule):
    """
    Class that represents a feed dashboard module.

    .. important::

        This class uses the 
        `Universal Feed Parser module <http://www.feedparser.org/>`_ to parse 
        the feeds, so you'll need to install it, all feeds supported by 
        FeedParser are thus supported by the FeedDashboardModule.

    As well as the ``DashboardModule`` properties, the ``FeedDashboardModule``
    takes two extra keyword arguments:

    ``feed_url``
        The URL of the feed.

    ``limit``
        The maximum number of feed entries to display. Default value: None, 
        which means that all entries are displayed.

    Here's a small example of building a recent actions module::
        
        from admin_tools.dashboard.models import *
        
        mydashboard = Dashboard()
        # will only list the django.contrib apps
        mydashboard.append(FeedDashboardModule(
            title=_('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

    The screenshot of what this code produces:

    .. image:: images/feed_dashboard_module.png
    """
    def __init__(self, *args, **kwargs):
        super(FeedDashboardModule, self).__init__(*args, **kwargs)
        self.title = kwargs.get('title', _('RSS Feed'))
        self.template = kwargs.get('template', 'dashboard/modules/feed.html')
        self.feed_url = kwargs.get('feed_url')
        self.limit = kwargs.get('limit')

    def render(self, request):
        import datetime
        if self.feed_url is None:
            raise ValueError('You must provide a valid feed URL')
        try:
            import feedparser
        except ImportError:
            raise ImportError('You must install the feedparser python module')

        feed = feedparser.parse(self.feed_url)
        if self.limit is not None:
            entries = feed['entries'][:self.limit]
        else:
            entries = feed['entries']
        for entry in entries:
            entry.url = entry.link
            try:
                entry.date = datetime.date(*entry.updated_parsed[0:3])
            except:
                # no date for certain feeds
                pass
            self.entries.append(entry)


class DefaultIndexDashboard(Dashboard):
    """
    The default dashboard displayed on the admin index page.
    To change the default dashboard you'll have to type the following from the
    commandline in your project root directory::

        python manage.py customdashboard

    And then set the ``ADMIN_TOOLS_INDEX_DASHBOARD`` settings variable to 
    point to your custom index dashboard class.
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
    The default dashboard displayed on the applications index page.
    To change the default dashboard you'll have to type the following from the
    commandline in your project root directory::

        python manage.py customdashboard

    And then set the ``ADMIN_TOOLS_APP_INDEX_DASHBOARD`` settings variable to 
    point to your custom app index dashboard class.
    """
    def render(self, request):

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
