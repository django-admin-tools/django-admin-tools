django-admin-tools
==================

|build-status-image| |codecov-image| |documentation-status-image| |pypi-version| |py-versions|

Overview
--------

django-admin-tools is a collection of extensions/tools for the default django
administration interface, it includes:

* a full featured and customizable dashboard;
* a customizable menu bar;
* tools to make admin theming easier.

The code is hosted on `Github <https://github.com/django-admin-tools/django-admin-tools/>`_.

Django-admin-tools is generously documented, you can
`browse the documentation online
<https://django-admin-tools.readthedocs.io/>`_.
a good start is to read `the quickstart guide
<https://django-admin-tools.readthedocs.io/en/latest/quickstart.html>`_.

The project was created by `David Jean Louis <http://www.izimobil.org/>`_ and was previously hosted on `Bitbucket <http://bitbucket.org/izi/django-admin-tools/>`_.

Please join the `mailing list <http://groups.google.fr/group/django-admin-tools>`_ if you want to discuss of the future of django-admin-tools.

Requirements
------------

django-admin-tools is compatible with Django 1.11 LTS up to Django 4.0 as well Python 2.7, 3.5+.

For older python and django versions please use the 0.8.1 version of django-admin-tools which is available on Pypi.

Installation
------------

To install django-admin-tools, run the following command inside this directory:

    python setup.py install

If you have the Python **easy_install** utility available, you can also type
the following to download and install in one step::

    easy_install django-admin-tools

Or if you're using **pip**::

    pip install django-admin-tools

Or if you'd prefer you can simply place the included "admin_tools" directory
somewhere on your python path, or symlink to it from somewhere on your Python
path; this is useful if you're working from a Mercurial checkout.

An `installation guide <https://django-admin-tools.readthedocs.io/en/latest/installation.html>`_ is available in the documentation.

Documentation
-------------

`Extensive documentation <https://django-admin-tools.readthedocs.io/>`_ is available, it was made with the excellent `Sphinx program <http://sphinx.pocoo.org/>`_

Translations
------------

There is a `a transifex project <https://transifex.net/projects/p/django-admin-tools/>`_ for django-admin-tools.

Screenshots
-----------

The django admin login screen:

.. image:: http://www.izimobil.org/django-admin-tools/images/capture-1.png
   :alt: The django admin login screen


The admin index dashboard:

.. image:: http://www.izimobil.org/django-admin-tools/images/capture-2.png
   :alt: The admin index dashboard


The admin menu:

.. image:: http://www.izimobil.org/django-admin-tools/images/capture-3.png
   :alt: The admin menu

Dashboard modules can be dragged, collapsed, closed etc.:

.. image:: http://www.izimobil.org/django-admin-tools/images/capture-4.png
   :alt: Dashboard modules can be dragged, collapsed, closed etc.

The app index dashboard:

.. image:: http://www.izimobil.org/django-admin-tools/images/capture-5.png
   :alt: The app index dashboard


.. |build-status-image| image:: https://api.travis-ci.com/django-admin-tools/django-admin-tools.svg?branch=master
   :target: http://travis-ci.com/django-admin-tools/django-admin-tools?branch=master
   :alt: Travis build

.. |codecov-image| image:: https://codecov.io/gh/django-admin-tools/django-admin-tools/branch/master/graph/badge.svg?token=RtyqJORRby
   :target: https://codecov.io/gh/django-admin-tools/django-admin-tools

.. |pypi-version| image:: https://img.shields.io/pypi/v/django-admin-tools.svg
   :target: https://pypi.python.org/pypi/django-admin-tools
   :alt: Pypi version

.. |documentation-status-image| image:: https://readthedocs.org/projects/django-admin-tools/badge/?version=latest
   :target: http://django-admin-tools.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. |py-versions| image:: https://img.shields.io/pypi/pyversions/djangorestframework-datatables.svg
   :target: https://img.shields.io/pypi/pyversions/djangorestframework-datatables.svg
   :alt: Python versions

.. |dj-versions| image:: https://img.shields.io/pypi/djversions/djangorestframework-datatables.svg
   :target: https://img.shields.io/pypi/djversions/djangorestframework-datatables.svg
   :alt: Django versions
