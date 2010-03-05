"""
This module contains the base classes for the dashboard and dashboard modules.
"""

from django.db import models
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.utils.importlib import import_module
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from admin_tools.utils import AppListElementMixin


class DashboardPreferences(models.Model):
    """
    This model represents the dashboard preferences for a user.
    """
    user = models.ForeignKey('auth.User')
    data = models.TextField()

    def __unicode__(self):
        return "%s dashboard preferences" % self.user.username

    class Meta:
        db_table = 'admin_tools_dashboard_preferences'
        ordering = ('user',)
    

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
                css = ('/media/css/mydashboard.css',)
                js = ('/media/js/mydashboard.js',)

    Here's an example of a custom dashboard::

        from django.core.urlresolvers import reverse
        from django.utils.translation import ugettext_lazy as _
        from admin_tools.dashboard.models import *

        class MyDashboard(Dashboard):
            def __init__(self, **kwargs):
                # we want a 3 columns layout
                self.columns = 3

                # append an app list module for "Applications"
                self.children.append(AppListDashboardModule(
                    title=_('Applications'),
                    exclude_list=('django.contrib',),
                ))
        
                # append an app list module for "Administration"
                self.children.append(AppListDashboardModule(
                    title=_('Administration'),
                    include_list=('django.contrib',),
                ))
        
                # append a recent actions module
                self.children.append(RecentActionsDashboardModule(
                    title=_('Recent Actions'),
                    limit=5
                ))

    Below is a screenshot of the resulting dashboard:

    .. image:: images/dashboard_example.png
    """
    class Media:
        css = ()
        js  = ()

    def __init__(self, **kwargs):
        """
        Dashboard constructor.
        """
        self.title = kwargs.get('title', _('Dashboard'))
        self.template = kwargs.get('template', 'dashboard/dashboard.html')
        self.columns = kwargs.get('columns', 2)
        self.children = kwargs.get('children', [])

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

    It also provides two helper methods:

    ``get_app_model_classes()``
        Method that returns the list of model classes for the current app.

    ``get_app_content_types()``
        Method that returns the list of content types for the current app.

    If you want to provide custom app index dashboard, be sure to inherit from
    this class instead of the ``Dashboard`` class.

    Here's an example of a custom app index dashboard::

        from django.core.urlresolvers import reverse
        from django.utils.translation import ugettext_lazy as _
        from admin_tools.dashboard.models import *

        class MyAppIndexDashboard(AppIndexDashboard):
            def __init__(self, **kwargs):
                AppIndexDashboard.__init__(self, **kwargs)
                # we don't want a title, it's redundant
                self.title = ''

                # append a model list module that lists all models 
                # for the app
                self.children.append(ModelListDashboardModule(
                    title=self.app_title,
                    include_list=self.models,
                ))
        
                # append a recent actions module for the current app
                self.children.append(RecentActionsDashboardModule(
                    title=_('Recent Actions'),
                    include_list=self.models,
                    limit=5
                ))

    Below is a screenshot of the resulting dashboard:

    .. image:: images/dashboard_app_index_example.png
    """
    def __init__(self, app_title, models, **kwargs):
        super(AppIndexDashboard, self).__init__(**kwargs)
        self.app_title = app_title
        self.models = models
    
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
        return [ContentType.objects.get_for_model(c) for c \
                in self.get_app_model_classes()]

    def get_id(self):
        """
        Internal method used to distinguish different dashboards in js code.
        """
        return '%s-dashboard' % slugify(unicode(self.app_title))


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
    def __init__(self, **kwargs):
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
        self.children = kwargs.get('children', [])

    def init_with_context(self, context):
        """
        Like for the ``Dashboard`` class, dashboard modules have a 
        ``init_with_context`` method that is called with a 
        ``django.template.RequestContext`` instance as unique argument.

        This gives you enough flexibility to build complex modules, for 
        example, let's build a "history" dashboard module, that will list the 
        last ten visited pages::

            class HistoryDashboardModule(LinkListDashboardModule):
                def init_with_context(self, context):
                    self.title = 'History'
                    request = context['request']
                    # we use sessions to store the visited pages stack
                    history = request.session.get('history', [])
                    for item in history:
                        self.children.append(item)
                    # add the current page to the history
                    history.insert(0, {
                        'title': context['title'],
                        'url': request.META['PATH_INFO']
                    })
                    if len(history) > 10:
                        history = history[:10]
                    request.session['history'] = history

        Here's a screenshot of our history item:

        .. image:: images/history_dashboard_module.png
        """
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
        >>> mod.children.append('foo')
        >>> mod.is_empty()
        False
        >>> mod.children = []
        >>> mod.is_empty()
        True
        """
        return self.pre_content is None and \
               self.post_content is None and \
               len(self.children) == 0

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

    Link list modules children are simple python dictionaries that can have the
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

        class MyDashboard(Dashboard):
            def __init__(self, **kwargs): 
                Dashboard.__init__(self, **kwargs)

                self.children.append(LinkListDashboardModule(
                    layout='inline',
                    children=(
                        {
                            'title': 'Python website',
                            'url': 'http://www.python.org',
                            'external': True,
                            'description': 'Python programming language rocks !',
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

    def __init__(self, **kwargs):
        super(LinkListDashboardModule, self).__init__(**kwargs)
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

        class MyDashboard(Dashboard):
            def __init__(self, **kwargs): 
                Dashboard.__init__(self, **kwargs)

                # will only list the django.contrib apps
                self.children.append(AppListDashboardModule(
                    title='Administration',
                    include_list=('django.contrib',)
                ))
                # will list all apps except the django.contrib ones
                self.children.append(AppListDashboardModule(
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

    def __init__(self, **kwargs):
        super(AppListDashboardModule, self).__init__(**kwargs)
        self.title = kwargs.get('title', _('Applications'))
        self.template = kwargs.get('template',
                                   'dashboard/modules/app_list.html')
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])

    def init_with_context(self, context):
        request = context['request']
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
            self.children.append(apps[app])


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

        class MyDashboard(Dashboard):
            def __init__(self, **kwargs): 
                Dashboard.__init__(self, **kwargs)
        
                # will only list the django.contrib.auth models
                self.children.append(ModelListDashboardModule(
                    title='Authentication',
                    include_list=('django.contrib.auth',)
                ))

    The screenshot of what this code produces:

    .. image:: images/modellist_dashboard_module.png

    .. note::

        Note that this module takes into account user permissions, for 
        example, if a user has no rights to change or add a ``Group``, then
        the django.contrib.auth.Group model line will not be displayed.
    """

    def __init__(self, **kwargs):
        super(ModelListDashboardModule, self).__init__(**kwargs)
        self.title = kwargs.get('title', '')
        self.template = kwargs.get('template',
                                   'dashboard/modules/model_list.html')
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])

    def init_with_context(self, context):
        request = context['request']
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
            self.children.append(model_dict)

        # sort model list alphabetically
        self.children.sort(lambda x, y: cmp(x['title'], y['title']))


class RecentActionsDashboardModule(DashboardModule):
    """
    Module that lists the recent actions for the current user.
    As well as the ``DashboardModule`` properties, the
    ``RecentActionsDashboardModule`` takes three extra keyword arguments:

    ``include_list``
        A list of contenttypes (e.g. "auth.group" or "sites.site") to include,
        only recent actions that match the given contenttypes will be
        displayed.

    ``exclude_list``
        A list of contenttypes (e.g. "auth.group" or "sites.site") to exclude,
        recent actions that match the given contenttypes will not be
        displayed.

    ``limit``
        The maximum number of children to display. Default value: 10.

    Here's a small example of building a recent actions module::
        
        from admin_tools.dashboard.models import *
        
        class MyDashboard(Dashboard):
            def __init__(self, **kwargs): 
                Dashboard.__init__(self, **kwargs)

                # will only list the django.contrib apps
                self.children.append(RecentActionsDashboardModule(
                    title='Django CMS recent actions',
                    include_list=('cms.page', 'cms.cmsplugin',)
                ))

    The screenshot of what this code produces:

    .. image:: images/recentactions_dashboard_module.png
    """

    def __init__(self, **kwargs):
        super(RecentActionsDashboardModule, self).__init__(**kwargs)
        self.title = kwargs.get('title', _('Recent Actions'))
        self.template = kwargs.get('template',
                                   'dashboard/modules/recent_actions.html')
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])
        self.limit = kwargs.get('limit', 10)

    def init_with_context(self, context):
        from django.db.models import Q
        from django.contrib.admin.models import LogEntry

        request = context['request']

        def get_qset(list):
            qset = None
            for contenttype in list:
                if isinstance(contenttype, ContentType):
                    current_qset = Q(content_type__id=contenttype.id)
                else:
                    try:
                        app_label, model = contenttype.split('.')
                    except:
                        raise ValueError('Invalid contenttype: "%s"' % contenttype)
                    current_qset = Q(
                        content_type__app_label=app_label,
                        content_type__model=model
                    )
                if qset is None:
                    qset = current_qset
                else:
                    qset = qset | current_qset
            return qset

        if request.user is None:
            qs = LogEntry.objects.all()
        else:
            qs = LogEntry.objects.filter(user__id__exact=request.user.id)

        if self.include_list:
            qs = qs.filter(get_qset(self.include_list))
        if self.exclude_list:
            qs = qs.exclude(get_qset(self.exclude_list))

        self.children = qs.select_related('content_type', 'user')[:self.limit]
        if not len(self.children):
            self.pre_content = _('No recent actions.')


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
        The maximum number of feed children to display. Default value: None, 
        which means that all children are displayed.

    Here's a small example of building a recent actions module::
        
        from admin_tools.dashboard.models import *
        
        class MyDashboard(Dashboard):
            def __init__(self, **kwargs): 
                Dashboard.__init__(self, **kwargs)
 
                # will only list the django.contrib apps
                self.children.append(FeedDashboardModule(
                    title=_('Latest Django News'),
                    feed_url='http://www.djangoproject.com/rss/weblog/',
                    limit=5
                ))

    The screenshot of what this code produces:

    .. image:: images/feed_dashboard_module.png
    """
    def __init__(self, **kwargs):
        super(FeedDashboardModule, self).__init__(**kwargs)
        self.title = kwargs.get('title', _('RSS Feed'))
        self.template = kwargs.get('template', 'dashboard/modules/feed.html')
        self.feed_url = kwargs.get('feed_url')
        self.limit = kwargs.get('limit')

    def init_with_context(self, context):
        import datetime
        if self.feed_url is None:
            raise ValueError('You must provide a valid feed URL')
        try:
            import feedparser
        except ImportError:
            self.children.append({
                'title': ('You must install the FeedParser python module'),
                'warning': True,
            })
            return

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
            self.children.append(entry)


class DefaultIndexDashboard(Dashboard):
    """
    The default dashboard displayed on the admin index page.
    To change the default dashboard you'll have to type the following from the
    commandline in your project root directory::

        python manage.py customdashboard

    And then set the ``ADMIN_TOOLS_INDEX_DASHBOARD`` settings variable to 
    point to your custom index dashboard class.
    """ 
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # append a link list module for "quick links"
        self.children.append(LinkListDashboardModule(
            title=_('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
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
        self.children.append(AppListDashboardModule(
            title=_('Applications'),
            exclude_list=('django.contrib',),
        ))

        # append an app list module for "Administration"
        self.children.append(AppListDashboardModule(
            title=_('Administration'),
            include_list=('django.contrib',),
        ))

        # append a recent actions module
        self.children.append(RecentActionsDashboardModule(
            title=_('Recent Actions'),
            limit=5
        ))

        # append a feed module
        self.children.append(FeedDashboardModule(
            title=_('Latest Django News'),
            feed_url='http://www.djangoproject.com/rss/weblog/',
            limit=5
        ))

        # append another link list module for "support". 
        self.children.append(LinkListDashboardModule(
            title=_('Support'),
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
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(ModelListDashboardModule(
            title=self.app_title,
            include_list=self.models,
        ))

        # append a recent actions module
        self.children.append(RecentActionsDashboardModule(
            title=_('Recent Actions'),
            include_list=self.get_app_content_types(),
            limit=5
        ))
