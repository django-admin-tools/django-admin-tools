.. _testing:

Testing of django-admin-tools
=============================

This is information for developers of django-admin-tools itself.

Running tests
-------------
Run the `runtests.sh` script which is situated at the root dir of
django-admin-tools project.

Run all tests::

    $ ./runtests.sh

Run only unit tests::

    $ ./runtests.sh unit

Run only tests for specified app::

    $ ./runtests.sh dashboard

Run only one test case::

    $ ./runtests.sh dashboard.ManagementCommandTest

Run only one test::

    $ ./runtests.sh dashboard.ManagementCommandTest.test_customdashboard


Code coverage report
--------------------
Install django-coverage app::

    $ pip install django-coverage

Then run tests and open test_proj/_coverage/index.html file in browser.


Where tests live
----------------
Unit tests should be put into appropriate module's tests.py.
Functional/integration tests should be put somewhere into test_proj.
