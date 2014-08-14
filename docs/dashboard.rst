.. _dashboard:

The django-admin-tools dashboard and dashboard modules API
==========================================================

This section describe the API of the django-admin-tools dashboard and
dashboard modules.
Make sure you read this before creating your custom dashboard and
custom modules.

..note::
    If your layout seems to be broken or you have problems with
    included javascript files, you should try to reset your dashboard
    preferences (assuming a MySQL backend, the truncate command also works in postgress)::

        python manage.py dbshell
        mysql> truncate admin_tools_dashboard_preferences;

    For more information see `this issue
    <http://bitbucket.org/izi/django-admin-tools/issue/43/issues-with-dashboard-preferences-and/>`_.

.. module:: admin_tools.dashboard

The ``Dashboard`` class
-----------------------

.. autoclass:: admin_tools.dashboard.Dashboard
    :members:

The ``AppIndexDashboard`` class
-------------------------------

.. autoclass:: admin_tools.dashboard.AppIndexDashboard
    :members:

.. module:: admin_tools.dashboard.modules

The ``DashboardModule`` class
-----------------------------

.. autoclass:: admin_tools.dashboard.modules.DashboardModule
    :members:

The ``Group`` class
------------------------------------

.. autoclass:: admin_tools.dashboard.modules.Group
    :members:

The ``LinkList`` class
-------------------------------------

.. autoclass:: admin_tools.dashboard.modules.LinkList
    :members:

The ``AppList`` class
------------------------------------

.. autoclass:: admin_tools.dashboard.modules.AppList
    :members:

The ``ModelList`` class
--------------------------------------

.. autoclass:: admin_tools.dashboard.modules.ModelList
    :members:

The ``RecentActions`` class
------------------------------------------

.. autoclass:: admin_tools.dashboard.modules.RecentActions
    :members:

The ``Feed`` class
---------------------------------

.. autoclass:: admin_tools.dashboard.modules.Feed
    :members:
