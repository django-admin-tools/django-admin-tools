#!/bin/sh
default_tests='dashboard theming menu test_app'
if [ $# -eq 0 ]
then
    test_proj/manage.py test $default_tests
else
    test_proj/manage.py test $*
fi
