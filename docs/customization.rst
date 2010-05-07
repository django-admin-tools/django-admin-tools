.. _customization:

Customization of the django-admin-tools modules
===============================================

Introduction
------------

django-admin-tools is very easy to customize, you can override the
admin menu, the index dashboard and the app index dashboard.

For this django-admin-tools provides two management commands:
 * ``custommenu``
 * ``customdashboard``


Customizing the navigation menu
-------------------------------

To customize the admin menu, the first step is to do the following::
    
    python manage.py custommenu

This will create a file named ``menu.py`` in your project directory.
If for some reason you want another file name, you can do::

    python manage.py custommenu somefile.py

The created file contains a class that is a copy of the default menu,
it is named ``CustomMenu``, you can rename it if you want but if you do
so, make sure you put the correct class name in your ADMIN_TOOLS_MENU
settings variable.

.. note::
    You could have done the above by hand, without using the 
    ``custommenu`` management command, but it's simpler with it.


Now you need to tell django-admin-tools to use your custom menu instead 
of the default one, open your settings.py file and add the following::

    ADMIN_TOOLS_MENU = 'yourproject.menu.CustomMenu'

Obviously, you need to change "yourproject" to the real project name, 
if you have chosen a different file name or if you renamed the menu 
class, you'll also need to change the above string to reflect your 
modifications.

At this point the menu displayed in the admin is your custom menu, now 
you can read :ref:`the menu and menu items API documentation <menu>` 
to learn how to create your custom menu.


Customizing the dashboards
--------------------------

To customize the index and app index dashboards, the first step is to do
the following::
    
    python manage.py customdashboard

This will create a file named ``dashboard.py`` in your project directory.
If for some reason you want another file name, you can do::

    python manage.py customdashboard somefile.py

The created file contains two classes:
 * The ``CustomIndexDashboard`` class that corresponds to the admin 
   index page dashboard;
 * The ``CustomAppIndexDashboard`` class that corresponds to the 
   index page of each installed application.

You can rename theses classes  if you want but if you do so, make sure 
adjust the ``ADMIN_TOOLS_INDEX_DASHBOARD`` and 
``ADMIN_TOOLS_APP_INDEX_DASHBOARD`` settings variables to match your
class names.

.. note::
    You could have done the above by hand, without using the 
    ``customdashboard`` management command, but it's simpler with it.


Now you need to tell django-admin-tools to use your custom dashboard(s).
Open your settings.py file and add the following::

    ADMIN_TOOLS_INDEX_DASHBOARD = 'yourproject.dashboard.CustomIndexDashboard'
    ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'yourproject.dashboard.CustomAppIndexDashboard'

If you only want a custom index dashboard, you would just need the first
line. Obviously, you need to change "yourproject" to the real project name, 
if you have chosen a different file name or if you renamed the dashboard
classes, you'll also need to change the above string to reflect your 
modifications.

At this point the dashboards displayed in the index and the app index 
should be your custom dashboards, now you can read 
:ref:`the dashboard and dashboard modules API documentation <dashboard>` 
to learn how to create your custom dashboard.


Customizing the theme
---------------------

.. warning::
    The theming support is still very basic, do not rely too much on it for
    the moment.

This is very simple, just configure the ``ADMIN_TOOLS_THEMING_CSS`` to
point to your custom css file, for example::

    ADMIN_TOOLS_THEMING_CSS = 'css/theming.css'

A good start is to copy the 
``admin_tools/media/admin_tools/css/theming.css`` to your custom file and
to modify it to suits your needs.
