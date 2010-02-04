.. _quickstart:

Quick start guide
=================

Before installing django-admin-tools, you'll need to have a copy of
`Django <http://www.djangoproject.com>`_ already installed. For the
|version| release, Django 1.1 or newer is required.


Installing django-admin-tools
-----------------------------

There are several ways to install django-admin-tools, this is explained 
in :ref:`the installation section <installation>`.

For the impatient, the easier method is to install django-admin-tools via  
`easy_install <http://peak.telecommunity.com/DevCenter/EasyInstall>`_ 
or `pip <http://pip.openplans.org/>`_. 

Using ``easy_install``, type::

    easy_install -Z django-admin-tools

Note that the ``-Z`` flag is required, to tell ``easy_install`` not to
create a zipped package; zipped packages prevent certain features of
Django from working properly.

Using ``pip``, type::

    pip install django-admin-tools


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

Required settings
~~~~~~~~~~~~~~~~~

You must add the django-admin-tools modules to the ``INSTALLED_APPS`` 
setting of your project like this::

    INSTALLED_APPS = (
        'admin_tools.theming',
        'admin_tools.menu',
        'admin_tools.dashboard',
        'django.contrib.auth',
        'django.contrib.sites',
        'django.contrib.admin'
        # ...other installed applications...
    )

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

Note: it is very important that you put the admin_tools modules **before** 
the ``django.contrib.admin module``, because django-admin-tools overrides 
the default django admin templates, and this will not work otherwise.


Setting up the django-admin-tools media files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To do this you have two options:

* create a symbolic link to the django-admin-tools media files to your 
  ``MEDIA_ROOT`` directory, for example::

      ln -s /usr/local/lib/python2.6/dist-packages/admin_tools/media/admin_tools /path/to/yourproject/media/

* copy the django-admin-tools media files to your ``MEDIA_ROOT`` directory, 
  for example::
  
      cp -r /usr/local/lib/python2.6/dist-packages/admin_tools/media/admin_tools /path/to/yourproject/media/


Testing your new shiny admin interface
--------------------------------------

Congrats ! at this point you should have a working installation of 
django-admin-tools, now you can just login to your admin site and see what 
changed.

django-admin-tools if fully customizable, but this is out of the scope of 
this quickstart, to learn how to customize django-admin-tools modules 
please read :ref:`the customization section<customization>`.

