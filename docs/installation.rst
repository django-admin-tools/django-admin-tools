.. _installation:

Installation guide
==================

Requirements
------------

Before installing django-admin-tools, you'll need to have a copy of
`Django <http://www.djangoproject.com>`_ already installed. For the
|version| release, Django 1.11 or newer is required.

.. note::
    *Important note to users of django 1.10 or below:*
    starting from 0.9.0, django-admin-tools is *NOT* compatible with
    django <= 1.10. If you want, you can still use the 0.8.1 version
    that will always be available on Pypi.

For further information, consult the `Django download page
<http://www.djangoproject.com/download/>`_, which offers convenient
packaged downloads and installation instructions.

.. note::
    If you want to display feeds in the admin dashboard, using the
    ``FeedDashboardModule`` you need to install the
    `Universal Feed Parser module <http://www.feedparser.org/>`_.


Installing django-admin-tools
-----------------------------

There are several ways to install django-admin-tools:

* Automatically, via a package manager.

* Manually, by downloading a copy of the release package and
  installing it yourself.

* Manually, by performing a Mercurial checkout of the latest code.

It is also highly recommended that you learn to use `virtualenv
<http://pypi.python.org/pypi/virtualenv>`_ for development and
deployment of Python software; ``virtualenv`` provides isolated Python
environments into which collections of software (e.g., a copy of
Django, and the necessary settings and applications for deploying a
site) can be installed, without conflicting with other installed
software. This makes installation, testing, management and deployment
far simpler than traditional site-wide installation of Python
packages.


Automatic installation via a package manager
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Several automatic package-installation tools are available for Python;
the most popular are `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_ and `pip
<http://pip.openplans.org/>`_. Either can be used to install
django-admin-tools.

Using ``easy_install``, type::

    easy_install -Z django-admin-tools

Note that the ``-Z`` flag is required, to tell ``easy_install`` not to
create a zipped package; zipped packages prevent certain features of
Django from working properly.

Using ``pip``, type::

    pip install django-admin-tools

It is also possible that your operating system distributor provides a
packaged version of django-admin-tools. Consult your operating system's
package list for details, but be aware that third-party distributions
may be providing older versions of django-admin-tools, and so you
should consult the documentation which comes with your operating
system's package.


Manual installation from a downloaded package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer not to use an automated package installer, you can
download a copy of django-admin-tools and install it manually. The
latest release package can be downloaded from `django-admin-tools's
listing on the Python Package Index
<http://pypi.python.org/pypi/django-admin-tools/>`_.

Once you've downloaded the package, unpack it (on most operating
systems, simply double-click; alternately, type ``tar zxvf
django-admin-tools-X-Y-Z.tar.gz`` at a command line on Linux, Mac OS X
or other Unix-like systems). This will create the directory
``django-admin-tools-X-Y-Z``, which contains the ``setup.py``
installation script. From a command line in that directory, type::

    python setup.py install

.. note::
    On some systems you may need to execute this with administrative
    privileges (e.g., ``sudo python setup.py install``).


Manual installation from a git checkout
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you'd like to try out the latest in-development code, you can
obtain it from the django-admin-tools repository, which is hosted on
`Github <https://github.com/django-admin-tools/django-admin-tools>`_.
To obtain the latest code and documentation, you'll need to have
Git installed, at which point you can type::

    git clone https://github.com/django-admin-tools/django-admin-tools.git

This will create a copy of the django-admin-tools Git repository on your
computer; you can then add the ``django-admin-tools`` directory to your
Python import path, or use the ``setup.py`` script to install as a package.
