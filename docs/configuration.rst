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
`relevant django documentation <http://docs.djangoproject.com/en/1.1/intro/tutorial02/#activate-the-admin-site>`_.

.. important::
    It is required that you use the django 1.1 syntax to declare the 
    django admin urls, e.g.::

        urlpatterns = patterns('',
            (r'^admin/', include(admin.site.urls)),
        )

    The old url style ``(r'^admin/(.*)', admin.site.root)`` won't work.

Required settings
~~~~~~~~~~~~~~~~~

First make sure you have the following template context processors 
installed::

    TEMPLATE_CONTEXT_PROCESSORS = (
        # default template context processors
        'django.core.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',

        # django 1.2 only
        'django.contrib.messages.context_processors.messages', 

        # required by django-admin-tools
        'django.core.context_processors.request',
    )

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

Adding django-admin-tools to your urls.py file
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You'll need to add django-admin-tools to your urls.py file::

    urlpatterns = patterns('',
        url(r'^admin_tools/', include('admin_tools.urls')),
        #...other url patterns...
    )

Setting up the django-admin-tools media files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To do this you have two options:

* create a symbolic link to the django-admin-tools media files to your 
  ``MEDIA_ROOT`` directory, for example::

      ln -s /usr/local/lib/python2.6/dist-packages/admin_tools/media/admin_tools /path/to/yourproject/media/

* copy the django-admin-tools media files to your ``MEDIA_ROOT`` directory, 
  for example::
  
      cp -r /usr/local/lib/python2.6/dist-packages/admin_tools/media/admin_tools /path/to/yourproject/media/

django-admin-tools will look for the media directory in the following 
settings variables (and in this order):

* ``ADMIN_TOOLS_MEDIA_URL``;
* ``STATIC_URL``: use this if you are using django-staticfiles;
* ``MEDIA_URL``.


Here's an example config if you are using django development server:

``urls.py``::

    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/path/to/media'}),

``settings.py``::

    MEDIA_URL = '/site_media/'


Available settings variables
----------------------------

``ADMIN_TOOLS_MEDIA_URL``
    You can use this variable if you want to set the media url for 
    django-admin-tools to something different from your ``MEDIA_URL``.

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

