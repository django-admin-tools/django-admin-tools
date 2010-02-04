"""
This module contains the base classes for menu and menu items.
"""

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.text import capfirst
from admin_tools.utils import AppListElementMixin


class Menu(list):
    """
    Base class for menus.
    The Menu class is a simple python list that takes an optional keyword 
    argument ``template``.

    >>> m = Menu(template='foo.html')
    >>> m.template
    'foo.html'
    >>> m.append(MenuItem())
    >>> m.append(MenuItem())
    >>> len(m)
    2
    >>> m.pop().__class__.__name__
    'MenuItem'
    >>> len(m)
    1
    """

    class Media:
        css = {'all': 'menu.css'}
        js  = ()

    def __init__(self, *args, **kwargs):
        """
        Manu constructor, keyword argument:
        * ``template``: the path to the menu template (optional)
        """
        super(Menu, self).__init__()
        self.template = kwargs.get('template', 'menu/menu.html')

    def is_empty(self):
        """
        Return True if the menu is empty and false otherwise.
        """
        return len([i for i in self]) == 0


class MenuItem(list):
    """
    Base class for menu items.
    A menu item is a simple python list that takes some optional keywords
    arguments. Menu items can be nested.
    """

    def __init__(self, *args, **kwargs):
        """
        MenuItem module constructor, keywords arguments (all are optional):

        ``title``
            String that contains the menu item title, make sure you use the
            django gettext functions if your application is multilingual. 
            Default value: 'Untitled menu item'.

        ``url``
            String that contains the menu item URL.
            Default value: '#'.

        ``css_classes``
            A list of css classes to be added to the menu item ``li`` class 
            attribute. Default value: None.

        ``accesskey``
            The menu item accesskey. Default value: None.

        ``description``
            An optional string that will be used as the ``title`` attribute of 
            the menu-item ``a`` tag. Default value: None.

        ``template``
            The template to use to render the menu item.
            Default value: 'menu/item.html'.
        """
        super(MenuItem, self).__init__()
        self.title = kwargs.get('title', 'Untitled menu item')
        self.url = kwargs.get('url', '#')
        self.css_classes = kwargs.get('css_classes', [])
        self.accesskey = kwargs.get('accesskey')
        self.description = kwargs.get('description')
        self.template = kwargs.get('template', 'menu/item.html')

    def render(self, request):
        pass


class AppListMenuItem(MenuItem, AppListElementMixin):
    """
    Class that represents a menu item that lists installed apps.
    """

    def __init__(self, *args, **kwargs):
        super(AppListMenuItem, self).__init__(*args, **kwargs)
        self.include_list = kwargs.get('include_list', [])
        self.exclude_list = kwargs.get('exclude_list', [])

    def render(self, request):
        apps = {}
        for model, model_admin in admin.site._registry.items():
            perms = self._check_perms(request, model, model_admin)
            if not perms or not perms['change']:
                continue
            app_label = model._meta.app_label
            if app_label not in apps:
                apps[app_label] = {
                    'title': capfirst(app_label.title()),
                    'url': reverse('admin:app_list', args=(app_label,)),
                    'models': []
                }
            apps[app_label]['models'].append({
                'title': capfirst(model._meta.verbose_name_plural),
                'url': self._get_admin_change_url(model)
            })

        apps_sorted = apps.keys()
        apps_sorted.sort()
        for app in apps_sorted:
            app_dict = apps[app]
            item = MenuItem(title=app_dict['title'], url=app_dict['url'])
            # sort model list alphabetically
            apps[app]['models'].sort(lambda x, y: cmp(x['title'], y['title']))
            for model_dict in apps[app]['models']:
                item.append(MenuItem(**model_dict))
            self.append(item)
