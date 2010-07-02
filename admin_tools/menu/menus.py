from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from admin_tools.menu import items

class Menu(object):
    """
    This is the base class for creating custom navigation menus.
    A menu can have the following properties:

    ``template``
        A string representing the path to template to use to render the menu.
        As for any other template, the path must be relative to one of the
        directories of your ``TEMPLATE_DIRS`` setting.
        Default value: "admin_tools/menu/menu.html".

    ``children``
        A list of children menu items. All children items mus be instances of
        the :class:`~admin_tools.menu.items.MenuItem` class.

    If you want to customize the look of your menu and it's menu items, you
    can declare css stylesheets and/or javascript files to include when
    rendering the menu, for example::

        from admin_tools.menu import Menu

        class MyMenu(Menu):
            class Media:
                css = ('/media/css/mymenu.css',)
                js = ('/media/js/mymenu.js',)

    Here's a concrete example of a custom menu::

        from django.core.urlresolvers import reverse
        from admin_tools.menu import items, Menu

        class MyMenu(Menu):
            def __init__(self, **kwargs):
                super(MyMenu, self).__init__(**kwargs)
                self.children.append(
                    items.MenuItem(title='Home', url=reverse('admin:index'))
                )
                self.children.append(
                    items.AppList(title='Applications')
                )
                self.children.append(
                    items.MenuItem(
                        title='Multi level menu item',
                        children=[
                            items.MenuItem(title='Child 1', url='/foo/'),
                            items.MenuItem(title='Child 2', url='/bar/'),
                        ]
                    ),
                )

    Below is a screenshot of the resulting menu:

    .. image:: images/menu_example.png
    """

    class Media:
        css = ()
        js  = ()

    def __init__(self, **kwargs):
        """
        Menu constructor.
        """
        self.template = kwargs.get('template', 'admin_tools/menu/menu.html')
        self.children = kwargs.get('children', [])

    def init_with_context(self, context):
        """
        Sometimes you may need to access context or request variables to build
        your menu, this is what the ``init_with_context()`` method is for.
        This method is called just before the display with a
        ``django.template.RequestContext`` as unique argument, so you can
        access to all context variables and to the ``django.http.HttpRequest``.
        """
        pass


class DefaultMenu(Menu):
    """
    The default menu displayed by django-admin-tools.
    To change the default menu you'll have to type the following from the
    commandline in your project root directory::

        python manage.py custommenu

    And then set the ``ADMIN_TOOLS_MENU`` settings variable to point to your
    custom menu class.
    """
    def __init__(self, **kwargs):
        super(DefaultMenu, self).__init__(**kwargs)
        self.children.append(items.MenuItem(
            title=_('Dashboard'),
            url=reverse('admin:index')
        ))
        self.children.append(items.Bookmarks())
        self.children.append(items.AppList(
            title=_('Applications'),
            exclude_list=('django.contrib',)
        ))
        self.children.append(items.AppList(
            title=_('Administration'),
            include_list=('django.contrib',)
        ))
