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
    The Dashboard class is a simple python list that takes three optional 
    keywords arguments ``title``, ``template`` and ``columns``.

    >>> d = Dashboard(template='foo.html', columns=3)
    >>> d.template
    'foo.html'
    >>> d.columns
    3
    >>> d.append(DashboardModule())
    >>> d.append(DashboardModule())
    >>> len(d)
    2
    >>> d.pop().__class__.__name__
    'DashboardModule'
    >>> len(d)
    1
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
        Dashboard constructor, keyword argument:
        
        ``title``
            the title to display for your dashboard.
            Default value: 'Dashboard'.
        
        ``template``
            the path to the dashboard template.
            Default value: 'dashboard/dashboard.html'.

        ``columns``
            The number of columns for the dashboard. Default value: 2.
        """
        super(Dashboard, self).__init__()
        self.title = kwargs.get('title', _('Dashboard'))
        self.template = kwargs.get('template', 'dashboard/dashboard.html')
        self.columns = kwargs.get('columns', 2)


class AppIndexDashboard(Dashboard):
    """
    Class that represents an app index dashboard, it is very similar to the 
    standard dashboard except that its constructors receives two arguments:

    ``app_title``
        The title of the application

    ``models``
        A list of strings representing the available models for the current 
        application, example::
            
            ['yourproject.app.Model1', 'yourproject.app.Model2']

    If you want to provide custom app index dashboard, be sure to inherit from
    this class instead of the ``Dashboard`` class.
    """
    def __init__(self, app_title, models, *args, **kwargs):
        super(AppIndexDashboard, self).__init__(*args, **kwargs)
        self.app_title = app_title
        self.models = models

class DashboardModule(object):
    """
    Base class for all dashboard modules.
    """
    def __init__(self, *args, **kwargs):
        """
        Dashboard module constructor, keywords arguments (all are optional):

        ``enabled``
            Boolean that determines whether the module should be enabled in 
            the dashboard by default or not. Default value: True.

        ``draggable``
            Boolean that determines whether the module can be draggable or not.
            Draggable modules can be re-arranged by users. Default value: True.

        ``collapsible``
            Boolean that determines whether the module is collapsible, this 
            allows users to show/hide module content. Default: True.

        ``deletable``
            Boolean that determines whether the module can be removed from the 
            dashboard by users or not. Default: True.

        ``title``
            String that contains the module title, make sure you use the django
            gettext functions if your application is multilingual. 
            Default value: ''.

        ``title_url``
            String that contains the module title URL. If given the module 
            title will be a link to this URL. Default value: None.

        ``css_classes``
            A list of css classes to be added to the module ``div`` class 
            attribute. Default value: None.

        ``pre_content``
            Text or HTML content to display above the module content.
            Default value: None.

        ``content``
            The module text or HTML content. Default value: None.

        ``post_content``
            Text or HTML content to display under the module content.
            Default value: None.

        ``template``
            The template to use to render the module.
            Default value: 'dashboard/module.html'.
        """
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
        self.entries = []

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


class TextDashboardModule(DashboardModule):
    """
    Dashboard module that displays a list of links.
    """

    def __init__(self, *args, **kwargs):
        super(TextDashboardModule, self).__init__(*args, **kwargs)
        self.entries.append(kwargs.get('text', ''))


class LinkListDashboardModule(DashboardModule):
    """
    Dashboard module that displays a list of links.
    """

    def __init__(self, *args, **kwargs):
        super(LinkListDashboardModule, self).__init__(*args, **kwargs)
        self.title = kwargs.get('title', _('Links'))
        self.template = kwargs.get('template',
                                   'dashboard/modules/link_list.html')
        self.layout = kwargs.get('layout', 'stacked')
        self.entries = kwargs.get('link_list', [])


class AppListDashboardModule(DashboardModule, AppListElementMixin):
    """
    Class that represents a dashboard module that lists installed apps.
    """

    def __init__(self, *args, **kwargs):
        super(AppListDashboardModule, self).__init__(*args, **kwargs)
        self.title = kwargs.get('title', _('Applications'))
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])
        self.template = kwargs.get('template',
                                   'dashboard/modules/app_list.html')

    def render(self, request):
        apps = {}
        for model, model_admin in admin.site._registry.items():
            perms = self._check_perms(request, model, model_admin)
            if not perms:
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

    def __init__(self, *args, **kwargs):
        super(ModelListDashboardModule, self).__init__(*args, **kwargs)
        self.title = kwargs.get('title', '')
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])
        self.template = kwargs.get('template',
                                   'dashboard/modules/model_list.html')

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
    """

    def __init__(self, *args, **kwargs):
        super(RecentActionsDashboardModule, self).__init__(*args, **kwargs)
        self.title = kwargs.get('title', _('Recent Actions'))
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])
        self.limit = kwargs.get('limit', [])
        self.template = kwargs.get('template',
                                   'dashboard/modules/recent_actions.html')

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
