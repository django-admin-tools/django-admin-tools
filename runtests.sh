#!/bin/sh
default_unit='admin_tools dashboard theming menu'
default_all="$default_unit test_app"
if [ $# -eq 0 ]
then
    test_proj/manage.py test $default_all
else
    if [ $1 = 'unit' ]
    then
        test_proj/manage.py test $default_unit
    else
        test_proj/manage.py test $*
    fi
fi
