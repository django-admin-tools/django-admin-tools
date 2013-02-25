.. _configuration:

Configuring django-admin-tools
==============================

Basic configuration
-------------------

Once installed, you can add django-admin-tools to any Django-based
project you're developing.

django-admin-tools is composed of several modules:

* admin_tools.theming: an app that makes it easy to customize the look
  and feel of the admin interface;

* admin_tools.menu: a customizable navigation menu that sits on top of
  every django administration index page;

* admin_tools.dashboard: a customizable dashboard that replaces the django
  administration index page.

Prerequisite
~~~~~~~~~~~~

In order to use django-admin-tools you obviously need to have configured
your django admin site, if you didn't, please refer to the
`relevant django documentation <https://docs.djangoproject.com/en/dev/intro/tutorial02/>`_.

Required settings
~~~~~~~~~~~~~~~~~

First make sure you have the ``django.core.context_processors.request``
template context processor in your ``TEMPLATE_CONTEXT_PROCESSORS``.

Then, add the django-admin-tools modules to the ``INSTALLED_APPS`` like
this::

    INSTALLED_APPS = (
        'admin_tools.theming',
        'admin_tools.menu',
        'admin_tools.dashboard',
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.admin'
        # ...other installed applications...
    )

.. note::
    it is very important that you put the admin_tools modules **before**
    the ``django.contrib.admin module``, because django-admin-tools
    overrides the default django admin templates, and this will not work
    otherwise.

django-admin-tools is modular, so if you want to disable a particular
module, just remove or comment it in your ``INSTALLED_APPS``.
For example, if you just want to use the dashboard::

    INSTALLED_APPS = (
        'admin_tools.dashboard',
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.admin'
        # ...other installed applications...
    )

Setting up the database
~~~~~~~~~~~~~~~~~~~~~~~

To set up the tables that django-admin-tools uses you'll need to type::

    python manage.py syncdb

django-admin-tools supports `South <http://south.aeracode.org>`_, so if you
have South installed, make sure you run the following commands::

    python manage.py migrate admin_tools.dashboard
    python manage.py migrate admin_tools.menu

Adding django-admin-tools to your urls.py file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You'll need to add django-admin-tools to your urls.py file::

    urlpatterns = patterns('',
        url(r'^admin_tools/', include('admin_tools.urls')),
        #...other url patterns...
    )

Available settings variables
----------------------------

``ADMIN_TOOLS_MENU``
    The path to your custom menu class, for example
    "yourproject.menu.CustomMenu".

``ADMIN_TOOLS_INDEX_DASHBOARD``
    The path to your custom index dashboard, for example
    "yourproject.dashboard.CustomIndexDashboard".

``ADMIN_TOOLS_APP_INDEX_DASHBOARD``
    The path to your custom app index dashboard, for example
    "yourproject.dashboard.CustomAppIndexDashboard".

``ADMIN_TOOLS_THEMING_CSS``
    The path to your theming css stylesheet, relative to your MEDIA_URL,
    for example::

        ADMIN_TOOLS_THEMING_CSS = 'css/theming.css'

