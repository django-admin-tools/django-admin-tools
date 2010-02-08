"""
This module contains the base classes for menu and menu items.
"""

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _
from admin_tools.utils import AppListElementMixin


class Menu(list):
    """
    Base class for menus.
    The Menu class is a simple python list that has an extra property:
    
    ``template``
        The template to use to render the menu.
        Default value: "menu/menu.html".

    If you want to customize the look of your menu and it's menu items, you
    can declare css stylesheets and/or javascript files to include when 
    rendering the menu, for example::

        from admin_tools.menu.models import *

        class MyMenu(Menu):
            class Media:
                css = {'screen': '/media/css/mymenu.css'}
                js = ('/media/js/mymenu.js',)

    Here's an example of a custom menu::

        from admin_tools.menu.models import *

        class MyMenu(Menu):
            def render(self, request):
                self.append(MenuItem(title='Home', url=reverse('admin:index')))
                self.append(AppListMenuItem(title='Applications'))
                item = MenuItem('Multi level menu item')
                item.append(MenuItem('Child 1'))
                item.append(MenuItem('Child 2'))
                self.append(item)

    Below is a screenshot of the resulting menu:

    .. image:: images/menu_example.png
    """

    class Media:
        css = {
            'all': 'menu.css',
            'ie' : 'menu-ie.css'
        }
        js  = ()

    def __init__(self, *args, **kwargs):
        """
        Manu constructor, keyword argument:
        * ``template``: the path to the menu template (optional)
        """
        super(Menu, self).__init__()
        self.template = kwargs.get('template', 'menu/menu.html')

    def render(self, request):
        """
        The ``Menu.render()`` method is called just before the display with a 
        ``django.http.HttpRequest`` as unique argument.
        Override this method to build your menu if you need to access to the
        request instance.
        """
        pass


class MenuItem(list):
    """
    Base class for menu items.
    A menu item is a simple python list that has some additional properties:

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

    Menu items can be nested so for example you can do the following::

        from admin_tools.menu.models import *

        mymenu = Menu()
        item = MenuItem(title='Foo')
        item.append(MenuItem(title='Bar'))
        mymenu.append(item)
    """

    def __init__(self, *args, **kwargs):
        super(MenuItem, self).__init__()
        self.title = kwargs.get('title', 'Untitled menu item')
        self.url = kwargs.get('url', '#')
        self.css_classes = kwargs.get('css_classes', [])
        self.accesskey = kwargs.get('accesskey')
        self.description = kwargs.get('description')
        self.template = kwargs.get('template', 'menu/item.html')

    def render(self, request):
        """
        The ``MenuItem.render()`` is called just before the display with a 
        ``django.http.HttpRequest`` as unique argument.
        You can use it to build your item when you need to access the request
        instance, for example::

            from admin_tools.menu.models import *
        
            class MyMenuItem(MenuItem):
                def render(self, request):
                    if request.user.username == 'foo':
                        self.title = 'Foo'
                    else:
                        self.title = 'Bar'

            mymenu = Menu()
            mymenu.append(MyMenuItem())
        """
        pass


class AppListMenuItem(MenuItem, AppListElementMixin):
    """
    A menu item that lists installed apps an their models.
    As well as the ``MenuItem`` properties, the ``AppListMenuItem`` has two
    extra properties:

    ``exclude_list``
        A list of apps to exclude, if an app name (e.g. "django.contrib.auth"
        starts with an element of this list (e.g. "django.contrib") it won't
        appear in the menu item.

    ``include_list``
        A list of apps to include, only apps whose name (e.g. 
        "django.contrib.auth") starts with one of the strings (e.g. 
        "django.contrib") in the list will appear in the menu item.

    If no include/exclude list is provided, **all apps** are shown.

    Here's a small example of building an app list menu item::
 
        from admin_tools.menu.models import *
     
        mymenu = Menu()

        # will list all apps except the django.contrib ones
        mymenu.append(AppListMenuItem(
            title='Applications',
            exclude_list=('django.contrib',)
        ))   

    The screenshot of what this code produces:

    .. image:: images/applist_menu_item.png

    .. note::

        Note that this module takes into account user permissions, for 
        example, if a user has no rights to change or add a ``Group``, then
        the django.contrib.auth.Group model child item will not be displayed.
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


class DefaultMenu(Menu):
    """
    The default menu displayed by default by django-admin-tools.
    To change the default menu you'll have to type the following from the
    commandline in your project root directory::

        python manage.py custommenu

    And then set the ``ADMIN_TOOLS_MENU`` settings variable to point to your
    custom menu class.
    """
    def render(self, request):
        self.append(MenuItem(
            title=_('Dashboard'),
            url=reverse('admin:index')
        ))
        self.append(AppListMenuItem(
            title=_('Applications'),
            exclude_list=('django.contrib',),
        ))
        self.append(AppListMenuItem(
            title=_('Administration'),
            include_list=('django.contrib',),
        ))
