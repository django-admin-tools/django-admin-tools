.. _testing:

Testing of django-admin-tools
=============================

This is information for developers of django-admin-tools itself.

Running tests
-------------

First, cd the test_proj directory::

    $ cd test_proj

And to run the tests, just type::

    $ python manage.py test


Code coverage report
--------------------
Install the coverage.py library and the django-coverage app::

    $ pip install coverage django-coverage

Then run tests and open test_proj/_coverage/index.html file in browser.


Where tests live
----------------
Unit tests should be put into appropriate module's tests.py.
Functional/integration tests should be put somewhere into test_proj.
