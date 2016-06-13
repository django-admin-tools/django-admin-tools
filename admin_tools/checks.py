from django.core.checks import register, Warning
from django.template.loader import get_template, TemplateDoesNotExist


W001 = Warning(
    'You must add "admin_tools.template_loaders.Loader" in your '
    'template loaders variable, see: '
    'https://django-admin-tools.readthedocs.io/en/latest/configuration.html',
    id='admin_tools.W001',
    obj='admin_tools'
)


@register('admin_tools')
def check_admin_tools_configuration(app_configs=None, **kwargs):
    result = []
    try:
        get_template('admin:admin/base.html')
    except TemplateDoesNotExist:
        result.append(W001)
    return result
