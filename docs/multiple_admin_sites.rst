.. _multiple_admin_sites:

Working with multiple admin sites
=================================

Introduction
------------

Django supports custom admin sites, and of course you can have as many
admin sites as you want, django-admin-tools provides basic support for
this, you can setup a custom dashboard for each admin site.

.. note::
    Multiple admin site support in django-admin-tools is, at the moment,
    limited to dashboards. This means you cannot have different menus or
    theming for each instance of admin sites. This will change in the near
    near future though.


Setting up a different dashboard for each admin site instance
-------------------------------------------------------------

In the following example we will assume that you have two admin site
instances: the default django admin site and a custom admin site of your
own. In your urls, you should have something like this::

    from django.conf.urls.defaults import *
    from django.contrib import admin
    from yourproject.admin import admin_site

    admin.autodiscover()

    urlpatterns = patterns('',
        (r'^admin/', include(admin.site.urls)),
        (r'^myadmin/', include(admin_site.urls)),
    )

Now to configure your dashboards, you could do::

    python manage.py customdashboard django_admin_dashboard.py
    python manage.py customdashboard my_admin_dashboard.py

And to tell django-admin-tools to use your custom dashboards depending on
the admin site being used, you just have to add the following to your project
settings file::

    ADMIN_TOOLS_INDEX_DASHBOARD = {
        'django.contrib.admin.site': 'yourproject.django_admin_dashboard.CustomIndexDashboard',
        'yourproject.admin.admin_site': 'yourproject.my_admin_dashboard.CustomIndexDashboard',
    }

Note that the same applies for the ``ADMIN_TOOLS_APP_INDEX_DASHBOARD``
settings variable.
