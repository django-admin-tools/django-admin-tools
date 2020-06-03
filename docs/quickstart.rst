.. _quickstart:

Quick start guide
=================

Before installing django-admin-tools, you'll need to have a copy of
`Django <http://www.djangoproject.com>`_ already installed. For the
|version| release, Django 1.11 or newer is required.

.. note::
    *Important note to users of django 1.6 or below:*
    starting from 0.6.0, django-admin-tools is *NOT* compatible with
    django <= 1.6. If you want, you can still use the 0.5.2 version
    that will always be available on Pypi.


Installing django-admin-tools
-----------------------------

django-admin-tools requires Django version 1.3 or superior, optionally,
if you want to display feed modules, you'll also need the
`Universal Feed Parser module <http://www.feedparser.org/>`_.

There are several ways to install django-admin-tools, this is explained
in :ref:`the installation section <installation>`.

For the impatient, the easiest method is to install django-admin-tools via
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
your Django admin site. If you didn't, please refer to the
`relevant django documentation <https://docs.djangoproject.com/en/dev/intro/tutorial02/>`_.

Configuration
~~~~~~~~~~~~~


First make sure you have the ``django.core.context_processors.request``
template context processor in your ``TEMPLATE_CONTEXT_PROCESSORS`` or
``TEMPLATES`` settings variable

Then add the ``admin_tools.template_loaders.Loader`` template loader to your
``TEMPLATE_LOADERS`` or ``TEMPLATES`` settings variable.

.. note::
    Windows users: due to filename restrictions on windows platforms, you
    have to put the ``admin_tools.template_loaders.Loader`` at the very
    beginning of the list in your ``TEMPLATES`` or ``TEMPLATE_LOADERS``
    settings variable.

Then, add admin_tools and its modules to the ``INSTALLED_APPS`` like this::

    INSTALLED_APPS = (
        'admin_tools',
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
    the ``django.contrib.admin`` module, because django-admin-tools
    overrides the default Django admin templates, and this will not work
    otherwise.

Then, just add django-admin-tools to your urls.py file::

    urlpatterns = patterns('',
        url(r'^admin_tools/', include('admin_tools.urls')),
        #...other url patterns...
    )

Finally simply run::

    python manage.py migrate

To collect static files run::

    python manage.py collectstatic

.. important::
    it is very important that ``django.contrib.staticfiles.finders.AppDirectoriesFinder``
    be there in your ``STATICFILES_FINDERS``.


Testing your new shiny admin interface
--------------------------------------

Congrats! At this point you should have a working installation of
django-admin-tools. Now you can just login to your admin site and see what
changed.

django-admin-tools is fully customizable, but this is out of the scope of
this quickstart. To learn how to customize django-admin-tools modules
please read :ref:`the customization section<customization>`.
