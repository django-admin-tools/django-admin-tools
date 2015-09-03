"""
django-admin-tools is a collection of extensions/tools for the default django 
administration interface, it includes:

 * a full featured and customizable dashboard,
 * a customizable menu bar,
 * tools to make admin theming easier.
"""
VERSION = '0.6.0'

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

# perform some configuration checks
if getattr(settings, 'TEMPLATES'):
    context_processors_var_name = loaders_var_name = 'TEMPLATES'
    context_processors = []
    loaders = []
    for engine in settings.TEMPLATES:
        if 'OPTIONS' in engine:
            if 'context_processors' in engine['OPTIONS']:
                context_processors += engine['OPTIONS']['context_processors']
            if 'loaders' in engine['OPTIONS']:
                loaders += engine['OPTIONS']['loaders']
else:
    context_processors_var_name = 'TEMPLATE_CONTEXT_PROCESSORS'
    loaders_var_name = 'TEMPLATE_LOADERS'
    context_processors = settings.TEMPLATE_LOADERS
    loaders = settings.TEMPLATE_LOADERS

if 'django.template.context_processors.request' not in context_processors:
    raise ImproperlyConfigured(
        'You must add the "django.template.context_processors.request" '
        'template context processor to your %s settings variable' % \
        context_processors_var_name
    )

if 'admin_tools.template_loaders.Loader' not in loaders:
    raise ImproperlyConfigured(
        'You must add the "admin_tools.template_loaders.Loader" template '
        'loader to your %s settings variable' % loaders_var_name
    )
