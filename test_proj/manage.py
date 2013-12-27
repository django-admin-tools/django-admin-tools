#!/usr/bin/env python

import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

import django


def manage_16ormore():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


def manage_15orless():
    from django.core.management import execute_manager
    try:
        import settings # Assumed to be in the same directory.
    except ImportError:
        sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.exit(1)

    execute_manager(settings)

if __name__ == "__main__":
    if django.VERSION > (1, 6):
        manage_16ormore()
    else:
        manage_15orless()
