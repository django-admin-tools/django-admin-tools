.. _quickstart:

Quick start guide
=================

Before installing django-admin-tools, you'll need to have a copy of
`Django <http://www.djangoproject.com>`_ already installed. For the
|version| release, Django 1.1 or newer is required.


Installing django-admin-tools
-----------------------------

django-admin-tools requires django version 1.1 or superior, optionally, 
if you want to display feed modules, you'll also need the 
`Universal Feed Parser module <http://www.feedparser.org/>`_.

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

For a more detailed guide on how to configure django-admin-tools, please
consult :ref:`the configuration section <configuration>`.

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
        'django.core.context_processors.auth',
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

.. important::
    it is very important that you put the admin_tools modules **before** 
    the ``django.contrib.admin module``, because django-admin-tools
    overrides the default django admin templates, and this will not work 
    otherwise.

django-admin-tools is modular, so if you want to disable a particular 
module, just remove or comment it in your ``INSTALLED_APPS``. 

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

