"""
Admin ui common utilities.
"""

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import capfirst

class AppListElementMixin(object):
    """
    Mixin class used by both the AppListDashboardModule and the 
    AppListMenuItem (to honor the DRY concept).
    """

    def _check_perms(self, request, model, model_admin):
        mod = '%s.%s' % (model.__module__, model.__name__)

        # check that the app is not in the exclude list
        for pattern in self.exclude_list:
            if mod.startswith(pattern):
                return False

        # check that the app is in the app list (if not empty)
        if len(self.include_list):
            found = False
            for pattern in self.include_list:
                if mod.startswith(pattern):
                    found = True
            if not found:
                return False

        # check that the user has module perms
        if not request.user.has_module_perms(model._meta.app_label):
            return False

        # check whether user has any perm for this module
        perms = model_admin.get_model_perms(request)
        if True not in perms.values():
            return False
        return perms

    def _get_app_title(self, model):
        app_name = model._meta.app_label.title()
        model_name = unicode(model._meta.verbose_name_plural)
        if app_name.rstrip('s').lower() == model_name.rstrip('s').lower():
            return capfirst(model_name)
        return '%s > %s' % (app_name, capfirst(model_name))

    def _get_admin_change_url(self, model):
        app_label = model._meta.app_label
        return reverse('admin:%s_%s_changelist' % (app_label,
                                                   model.__name__.lower()))

    def _get_admin_add_url(self, model):
        app_label = model._meta.app_label
        return reverse('admin:%s_%s_add' % (app_label, model.__name__.lower()))


# todo: refactor how menu and dashboard media are rendered
def render_media(type, tpl, obj):
    """
    Helper method used by the render_menu_css/js and render_dashboard_css/js 
    template tags.
    """
    p = getattr(settings, 'ADMIN_TOOLS_MEDIA_URL', getattr(settings, 'MEDIA_URL'))
    cache = []

    def get_css_include(o):
        ret = []
        for t, f in o.Media.css.items():
            if (t,f) not in cache:
                ret.append(tpl % (t, p, f))
                cache.append((t,f))
        return ret

    def get_js_include(o):
        ret = []
        for f in o.Media.js:
            if f not in cache:
                ret.append(tpl % (p, f))
                cache.append(f)
        return ret

    return "\n".join(locals()['get_%s_include' % type](obj))
