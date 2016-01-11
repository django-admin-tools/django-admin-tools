"""
Based on https://bitbucket.org/tzulberti/django-apptemplates/
and http://djangosnippets.org/snippets/1376/

Django template loader that allows you to load a template from a
specific application. This allows you to both extend and override
a template at the same time. The default Django loaders require you
to copy the entire template you want to override, even if you only
want to override one small block.

Template usage example::
    {% extends "admin:admin/base.html" %}
"""

from os.path import join

from django.apps import apps
from django.template.loaders.filesystem import Loader as FilesystemLoader

_cache = {}


def get_app_template_dir(app_name):
    """Get the template directory for an application

    Uses apps interface available in django 1.7+

    Returns a full path, or None if the app was not found.
    """
    if app_name in _cache:
        return _cache[app_name]
    template_dir = None
    for app in apps.get_app_configs():
        if app.label == app_name:
            template_dir = join(app.path, 'templates')
            break
    _cache[app_name] = template_dir
    return template_dir


class Loader(FilesystemLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name" in the specified app.
        If the name does not contain an app name (no colon), an empty list
        is returned.
        The parent FilesystemLoader.load_template_source() will take care
        of the actual loading for us.
        """
        if ':' not in template_name:
            return []
        app_name, template_name = template_name.split(":", 1)
        template_dir = get_app_template_dir(app_name)
        if template_dir:
            try:
                from django.template import Origin
                origin = Origin(
                    name=join(template_dir, template_name),
                    template_name=template_name,
                    loader=self,
                )
            except (ImportError, TypeError):
                origin = join(template_dir, template_name)
            return [origin]
        return []
