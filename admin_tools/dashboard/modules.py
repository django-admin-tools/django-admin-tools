from django.contrib import admin
from django.utils.text import capfirst
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from admin_tools.utils import AppListElementMixin


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
        Default value: 'admin_tools/dashboard/module.html'.
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
        self.template = kwargs.get('template', 'admin_tools/dashboard/module.html')
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
                                   'admin_tools/dashboard/modules/link_list.html')
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
                                   'admin_tools/dashboard/modules/app_list.html')
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
                                   'admin_tools/dashboard/modules/model_list.html')
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
                                   'admin_tools/dashboard/modules/recent_actions.html')
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
        self.template = kwargs.get('template', 'admin_tools/dashboard/modules/feed.html')
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


