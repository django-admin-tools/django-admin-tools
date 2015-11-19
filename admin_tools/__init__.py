"""
django-admin-tools is a collection of extensions/tools for the default django 
administration interface, it includes:

 * a full featured and customizable dashboard,
 * a customizable menu bar,
 * tools to make admin theming easier.
"""
VERSION = '0.7.0'


def check_configuration():
    """
    Perform some configuration checks for django-admin-tools.
    """
    try:
        templates = getattr(settings, 'TEMPLATES', False)
    except ImproperlyConfigured:
        # settings are not configured, don't bother
        return False

    if templates:
        processors_var_name = loaders_var_name = 'TEMPLATES'
        processors = []
        loaders = []
        for engine in settings.TEMPLATES:
            if 'OPTIONS' in engine:
                if 'context_processors' in engine['OPTIONS']:
                    processors += engine['OPTIONS']['context_processors']
                if 'loaders' in engine['OPTIONS']:
                    loaders += engine['OPTIONS']['loaders']
    else:
        processors_var_name = 'TEMPLATE_CONTEXT_PROCESSORS'
        loaders_var_name = 'TEMPLATE_LOADERS'
        processors = settings.TEMPLATE_CONTEXT_PROCESSORS
        loaders = settings.TEMPLATE_LOADERS

    for loader in loaders:
        if isinstance(loader, (tuple, list)):
            loaders += loader[1]
    
    if 'django.template.context_processors.request' not in processors and \
       'django.core.context_processors.request' not in processors:
        raise ImproperlyConfigured(
            'You must add the "django.template.context_processors.request" '
            'template context processor to your %s settings variable' % \
            processors_var_name
        )
    
    if 'admin_tools.template_loaders.Loader' not in loaders:
        raise ImproperlyConfigured(
            'You must add the "admin_tools.template_loaders.Loader" template '
            'loader to your %s settings variable' % loaders_var_name
        )

try:
    from django.conf import settings
    from django.core.exceptions import ImproperlyConfigured
    check_configuration()
except ImportError:
    pass
