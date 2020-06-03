django-admin-tools
==================

.. image:: https://travis-ci.org/django-admin-tools/django-admin-tools.svg?branch=master
   :target: https://travis-ci.org/django-admin-tools/django-admin-tools
   :alt: Build status
.. image:: https://codecov.io/gh/django-admin-tools/django-admin-tools/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/django-admin-tools/django-admin-tools
   :alt: Test coverage status
.. image:: https://img.shields.io/pypi/l/django-admin-tools.svg
.. image:: https://img.shields.io/pypi/pyversions/django-admin-tools.svg
.. image:: https://img.shields.io/badge/django-1.11%20or%20newer-green.svg

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

************
Requirements
************

django-admin-tools is compatible with Django 1.11 LTS, and 2.1+, 3.0 as well Python 2.7, 3.5+.

For older python and django versions please use the 0.8.1 version of django-admin-tools which is available on Pypi.

************
Installation
************

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

*************
Documentation
*************

`Extensive documentation <https://django-admin-tools.readthedocs.io/>`_ is available, it was made with the excellent `Sphinx program <http://sphinx.pocoo.org/>`_

************
Translations
************

There is a `a transifex project <https://transifex.net/projects/p/django-admin-tools/>`_ for django-admin-tools.

************
Screenshots
************

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

