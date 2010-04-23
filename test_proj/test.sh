#!/bin/sh

default_tests='dashboard theming menu test_app'
if [ $# -eq 0 ]
then
    ./manage.py test $default_tests
else
    ./manage.py test $*
fi
